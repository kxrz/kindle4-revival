#!/usr/bin/env python3
"""Sort a pile of EPUB files into Genre/Author/[Series NN - ]Title.epub.

Dry run by default: it prints the plan and writes nothing.

  python3 organize_library.py SRC [SRC ...] --dest /Volumes/Kindle/documents
  python3 organize_library.py SRC --dest DIR --config my-library.json --apply

What it does, using only the metadata inside each EPUB:
  - author: first dc:creator, rewritten as "Last, First"
  - title: dc:title, minus common download-site junk ("(French Edition)", years, ...)
  - series: calibre:series / EPUB3 belongs-to-collection, with its index
  - genre: config "authors" map, then dc:subject keywords, then --default-genre
  - duplicates (same author + title) are skipped, the largest file wins
Originals are never modified; files are copied.
Only the standard library is used.
"""
import argparse, collections, json, os, re, shutil, sys, unicodedata, zipfile
import xml.etree.ElementTree as ET

NS = {"dc": "http://purl.org/dc/elements/1.1/", "opf": "http://www.idpf.org/2007/opf"}
CONTAINER = "{urn:oasis:names:tc:opendocument:xmlns:container}rootfile"

# dc:subject keyword (lowercase, accents removed) -> genre. First match wins.
DEFAULT_SUBJECTS = [
    ("science fiction", "Science-fiction"), ("science-fiction", "Science-fiction"), ("sf", "Science-fiction"),
    ("fantasy", "Fantastique & fantasy"), ("fantastique", "Fantastique & fantasy"),
    ("horreur", "Fantastique & fantasy"), ("horror", "Fantastique & fantasy"),
    ("thriller", "Polar & thriller"), ("policier", "Polar & thriller"), ("polar", "Polar & thriller"),
    ("crime", "Polar & thriller"), ("mystery", "Polar & thriller"), ("suspense", "Polar & thriller"),
    ("espionnage", "Polar & thriller"),
    ("jeunesse", "Jeunesse"), ("young adult", "Jeunesse"), ("juvenile", "Jeunesse"),
    ("essai", "Essais & documents"), ("histoire", "Essais & documents"), ("biograph", "Essais & documents"),
    ("roman", "Littérature"), ("litterature", "Littérature"), ("fiction", "Littérature"),
]
JUNK = [
    r"\s*\((French Edition|ebook|\d{4})\)", r"\s*\(\d+ebooks\.[a-z]+\)", r"\s*-\s*libgen\.[a-z]+$",
    r"\s*--.*Anna.s Archive$", r"\s*\[.*?\]$", r",? en français\b.*$", r"\s*[—-]\s*Complete$",
    r"\s*\([^)]*\b(thriller|suspense|tome|livre|edition)\b[^)]*\)$", r":\s*(Un polar|Le thriller|Un thriller|Thriller|Histoire à suspense|Prix).*$",
]
PARTICLES = {"de", "le", "la", "van", "von", "du", "des", "di", "da", "del"}


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def key(s):
    return re.sub(r"[^a-z0-9]", "", strip_accents(s).lower())


def read_epub(path):
    z = zipfile.ZipFile(path)
    opf = ET.fromstring(z.read("META-INF/container.xml")).find(".//" + CONTAINER).get("full-path")
    md = ET.fromstring(z.read(opf)).find("opf:metadata", NS)
    get = lambda tag: [(e.text or "").strip() for e in md.findall("dc:" + tag, NS) if (e.text or "").strip()]
    meta = {"title": (get("title") or [""])[0], "author": (get("creator") or [""])[0], "subjects": get("subject")}
    for m in md.findall("opf:meta", NS):
        if m.get("name") == "calibre:series":
            meta["series"] = m.get("content")
        elif m.get("name") == "calibre:series_index":
            meta["series_index"] = m.get("content")
        elif m.get("property") == "belongs-to-collection":
            meta["series"] = (m.text or "").strip()
        elif m.get("property") == "group-position":
            meta["series_index"] = (m.text or "").strip()
    return meta


def norm_author(a):
    a = re.sub(r"\s+", " ", a.replace("_", ".")).strip(" .;,")
    a = a.split(";")[0].split(" & ")[0].strip()
    if not a:
        return "Inconnu"
    if "," in a:
        last, first = (x.strip() for x in a.split(",", 1))
    else:
        parts = a.split(" ")
        if len(parts) == 1:
            return a
        i = len(parts) - 1
        while i > 1 and parts[i - 1].lower() in PARTICLES:
            i -= 1
        first, last = " ".join(parts[:i]), " ".join(parts[i:])
    if last.isupper() and len(last) > 3:
        last = last.title()
    if first.isupper() and len(first) > 3:
        first = first.title()
    return f"{last}, {first}" if first else last


def clean_title(t):
    for pattern in JUNK:
        t = re.sub(pattern, "", t, flags=re.I)
    t = t.strip(" .-_")
    if t.isupper() and len(t) > 4:
        t = t.capitalize()
    return t[:1].upper() + t[1:]


def safe(s):
    """Make a string safe for a FAT32 (Kindle) file name."""
    s = s.replace(":", " -").replace("/", "-").replace("\\", "-").replace("?", "").replace('"', "'")
    s = re.sub(r"[*<>|]", "", s)
    return re.sub(r"\s+", " ", s).strip(" .")[:110]


def genre_for(author, subjects, title, cfg, default):
    if author in cfg.get("authors", {}):
        return cfg["authors"][author]
    words = [strip_accents(s).lower() for s in subjects] + [strip_accents(title).lower()]
    for kw, genre in cfg.get("subjects", DEFAULT_SUBJECTS):
        kw = strip_accents(kw).lower()
        if any(kw == w or (len(kw) > 3 and kw in w) for w in words):
            return genre
    return default


def build_plan(sources, cfg, default_genre):
    items, errors = {}, []
    for src in sources:
        for root, _, files in os.walk(src):
            for f in sorted(files):
                if not f.lower().endswith(".epub") or f.startswith("._"):
                    continue
                path = os.path.join(root, f)
                try:
                    m = read_epub(path)
                except Exception as e:
                    errors.append((path, repr(e)))
                    continue
                author = norm_author(m["author"])
                author = cfg.get("author_fixes", {}).get(author, author)
                title = cfg.get("title_fixes", {}).get(m["title"], clean_title(m["title"]))
                series, idx = m.get("series"), m.get("series_index")
                try:
                    idx = int(float(idx)) if idx else None
                except ValueError:
                    idx = None
                name = f"{series} {idx:02d} - {title}" if series and idx else title
                genre = genre_for(author, m["subjects"], m["title"], cfg, default_genre)
                item = {"src": path, "size": os.path.getsize(path),
                        "dst": os.path.join(safe(genre), safe(author), safe(name) + ".epub")}
                k = (key(author), key(title))
                if k in items and items[k]["size"] >= item["size"]:
                    items[k].setdefault("dupes", []).append(path)
                    continue
                if k in items:
                    item["dupes"] = [items[k]["src"]] + items[k].get("dupes", [])
                items[k] = item
    return list(items.values()), errors


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sources", nargs="+", help="folders containing EPUB files")
    ap.add_argument("--dest", required=True, help="destination, e.g. /Volumes/Kindle/documents")
    ap.add_argument("--config", help="JSON file with authors / author_fixes / title_fixes / subjects")
    ap.add_argument("--default-genre", default="Littérature")
    ap.add_argument("--apply", action="store_true", help="really copy the files")
    ap.add_argument("--report", help="write the source -> destination mapping to this file")
    a = ap.parse_args()

    cfg = json.load(open(a.config, encoding="utf-8")) if a.config else {}
    plan, errors = build_plan(a.sources, cfg, a.default_genre)
    plan.sort(key=lambda p: strip_accents(p["dst"]).lower())

    for p in plan:
        print(p["dst"])
    counts = collections.Counter(p["dst"].split(os.sep)[0] for p in plan)
    print(f"\n{len(plan)} books, {sum(len(p.get('dupes', [])) for p in plan)} duplicates skipped, "
          f"{sum(p['size'] for p in plan) // 2**20} MB", file=sys.stderr)
    for g, n in counts.most_common():
        print(f"  {n:4d}  {g}", file=sys.stderr)
    for path, err in errors:
        print(f"  unreadable: {path}: {err}", file=sys.stderr)

    if a.report:
        with open(a.report, "w", encoding="utf-8") as f:
            for p in plan:
                for s in [p["src"]] + p.get("dupes", []):
                    f.write(f"{p['dst']}\t{s}\n")
    if not a.apply:
        print("\nDry run: nothing copied. Add --apply to copy.", file=sys.stderr)
        return
    copied = 0
    for p in plan:
        dst = os.path.join(a.dest, p["dst"])
        if os.path.exists(dst) and os.path.getsize(dst) == p["size"]:
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(p["src"], dst)
        copied += 1
    print(f"{copied} files copied to {a.dest}", file=sys.stderr)


if __name__ == "__main__":
    main()
