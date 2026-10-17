# kindle4-revival

**Jailbreak a Kindle 4 (non-touch, firmware 4.x) in 2026, install KOReader, French dictionaries and a tidy library.**
Tested on a 2011 Kindle 4 running firmware 4.1.4, in October 2026.

🇫🇷 [Version française](README.fr.md)

Most Kindle 4 tutorials online are out of date: they point to tools for newer models, or predate the April 2025 certificate expiry that broke KUAL. This repository holds the steps that worked, the exact files, and the small tools I wrote along the way.

## Read the guide

- 🇬🇧 [How I jailbroke my Kindle 4 in 2026](articles/kindle-4-jailbreak-2026.en.md)
- 🇫🇷 [Jailbreaker une Kindle 4 en 2026 : le guide qui marche vraiment](articles/kindle-4-jailbreak-2026.fr.md)

## The short version

| # | Step | Details |
|---|---|---|
| 0 | `./scripts/fetch-files.sh` | downloads every file below and checks its SHA-256 |
| 1 | Check the firmware is **4.x** and the serial starts with **B00E** or **B023** | otherwise this is the wrong guide |
| 2 | Copy `data.tar.gz`, `ENABLE_DIAGS`, `diagnostic_logs/` from `K4-Jailbreak.zip` to the Kindle root, restart, then **D → R → left** | "You are Jailbroken" appears |
| 3 | Copy `KUAL-KDK-1.0.azw2` to `documents/` | open it like a book |
| 4 | KUAL crashes with a *RuntimeException*? | run [`tools/fix-kual-booklet`](tools/fix-kual-booklet/runme.sh) |
| 5 | Unzip `koreader-kindle-*.zip` at the Kindle root | KUAL → KOReader → Start KOReader (no framework) |
| 6 | Unpack the dictionaries into `koreader/data/dict/<name>/` | one folder per dictionary |
| 7 | Sort your EPUBs with [`tools/organize-library`](tools/organize-library/) | then set KOReader's display mode to show file names |

![Diagnosis: KUAL crash log](docs/img/03-kual-crash-log.svg)

## What's in here

```
articles/           the full guide, English and French
docs/img/           terminal captures (generated from docs/transcripts/ with scripts/term2svg.py)
files/              third-party files, downloaded by scripts/fetch-files.sh (not committed)
scripts/            fetch-files.sh, term2svg.py
tools/
  diagnostic/       read-only system report, run by the jailbreak as runme.sh
  fix-kual-booklet/ removes a stray KUALBooklet.jar that breaks KUAL on a Kindle 4
  kual-screenshot/  KUAL extension that captures the screen, plus a PNG converter
  organize-library/ sorts EPUBs into Genre/Author/Series NN - Title.epub
```

## Files used

| File | Version | License | Upstream |
|---|---|---|---|
| K4-Jailbreak.zip | v1.0.0 (2026-06-29) | none stated | [KindleModding/K4-Jailbreak](https://github.com/KindleModding/K4-Jailbreak) |
| KUAL-KDK-1.0.azw2 | v2.7.37 (2025-04-19) | MIT / Apache-2.0 | [MobileRead, NiLuJe's snapshots](https://www.mobileread.com/forums/showthread.php?t=225030) |
| koreader-kindle-v2026.07.1.zip | v2026.07.1 | AGPL-3.0 | [koreader/koreader](https://github.com/koreader/koreader) |
| fr-fr.tar.zst, en-fr.tar.zst | release 20261016 | GPL-3.0 (tool), CC BY-SA (Wiktionary data) | [xxyzz/wiktionary_stardict](https://github.com/xxyzz/wiktionary_stardict) |

These files are not committed: `scripts/fetch-files.sh` downloads them from their upstream and verifies the checksums. All credit goes to their authors, NiLuJe and the MobileRead community, KindleModding, and the KOReader team.

## Disclaimer

Jailbreaking modifies the device's system. The risk is low with this method but not zero. Do it on a device you own. Nothing here bypasses DRM: KOReader only opens DRM-free books.
