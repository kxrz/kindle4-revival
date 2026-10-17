# organize-library

Sorts EPUB files into a folder tree that is easy to browse on a Kindle without a touchscreen:

```
Genre/Last, First/Series NN - Title.epub
```

Standard library only (Python 3.8+). Originals are never modified, files are copied.

```sh
# 1. dry run: prints the plan, writes nothing
python3 organize_library.py ~/Books/batch1 ~/Books/batch2 --dest /Volumes/Kindle/documents

# 2. fix what the guessing got wrong in a JSON file, then copy
python3 organize_library.py ~/Books/* --dest /Volumes/Kindle/documents --config my-library.json --apply
```

- **Author**: first `dc:creator`, rewritten as `Last, First`.
- **Title**: `dc:title` without common junk (`(French Edition)`, years, site names, marketing after a colon).
- **Series**: `calibre:series` or EPUB 3 `belongs-to-collection`, with the index.
- **Genre**: the `authors` map of the config, then `dc:subject` and title keywords, then `--default-genre`.
- **Duplicates**: same author and title, the largest file wins. `--report mapping.tsv` writes source → destination.

Config keys (all optional), see [`example-config.json`](example-config.json):

| Key | Meaning |
|---|---|
| `authors` | `"Last, First": "Genre"` |
| `author_fixes` | `"wrong form": "Last, First"` |
| `title_fixes` | `"raw dc:title": "clean title"` |
| `subjects` | list of `[keyword, genre]`, replaces the built-in list |

After copying, set KOReader's file browser **Display mode** to *Detailed list with cover images and filenames* (or *Classic*), otherwise it shows the raw metadata titles instead of the clean file names.
