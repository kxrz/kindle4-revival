# kindle4-revival

**Jailbreaker une Kindle 4 (sans écran tactile, firmware 4.x) en 2026, installer KOReader, des dictionnaires français et une bibliothèque rangée.**
Testé sur une Kindle 4 de 2011 en firmware 4.1.4, en octobre 2026.

🇬🇧 [English version](README.md)

La plupart des tutoriels pour Kindle 4 sont périmés : ils renvoient vers des outils pour d'autres modèles, ou datent d'avant l'expiration des certificats d'avril 2025 qui a cassé KUAL. Ce dépôt réunit les étapes qui ont marché, les fichiers exacts et les petits outils écrits en chemin.

## Lire le guide

- 🇫🇷 [Jailbreaker une Kindle 4 en 2026 : le guide qui marche vraiment](articles/kindle-4-jailbreak-2026.fr.md)
- 🇬🇧 [How I jailbroke my Kindle 4 in 2026](articles/kindle-4-jailbreak-2026.en.md)

## La version courte

| # | Étape | Détail |
|---|---|---|
| 0 | `./scripts/fetch-files.sh` | télécharge tous les fichiers ci-dessous et vérifie leur SHA-256 |
| 1 | Vérifier que le firmware est en **4.x** et que le numéro de série commence par **B00E** ou **B023** | sinon, ce n'est pas le bon guide |
| 2 | Copier `data.tar.gz`, `ENABLE_DIAGS`, `diagnostic_logs/` de `K4-Jailbreak.zip` à la racine, redémarrer, puis **D → R → gauche** | « You are Jailbroken » apparaît |
| 3 | Copier `KUAL-KDK-1.0.azw2` dans `documents/` | il s'ouvre comme un livre |
| 4 | KUAL plante avec une *RuntimeException* ? | lancer [`tools/fix-kual-booklet`](tools/fix-kual-booklet/runme.sh) |
| 5 | Décompresser `koreader-kindle-*.zip` à la racine | KUAL → KOReader → Start KOReader (no framework) |
| 6 | Décompresser les dictionnaires dans `koreader/data/dict/<nom>/` | un dossier par dictionnaire |
| 7 | Ranger ses EPUB avec [`tools/organize-library`](tools/organize-library/) | puis régler l'affichage de KOReader sur les noms de fichiers |

![Diagnostic : le journal d'erreur de KUAL](docs/img/03-kual-crash-log.svg)

## Contenu

```
articles/           le guide complet, en français et en anglais
docs/img/           captures de terminal (générées depuis docs/transcripts/ avec scripts/term2svg.py)
files/              fichiers tiers, téléchargés par scripts/fetch-files.sh (non versionnés)
scripts/            fetch-files.sh, term2svg.py
tools/
  diagnostic/       rapport système en lecture seule, exécuté par le jailbreak (runme.sh)
  fix-kual-booklet/ supprime un KUALBooklet.jar qui casse KUAL sur Kindle 4
  kual-screenshot/  extension KUAL de capture d'écran, et son convertisseur PNG
  organize-library/ range des EPUB en Genre/Auteur/Série NN - Titre.epub
```

## Fichiers utilisés

| Fichier | Version | Licence | Source |
|---|---|---|---|
| K4-Jailbreak.zip | v1.0.0 (29/06/2026) | non précisée | [KindleModding/K4-Jailbreak](https://github.com/KindleModding/K4-Jailbreak) |
| KUAL-KDK-1.0.azw2 | v2.7.37 (19/04/2025) | MIT / Apache-2.0 | [MobileRead, snapshots de NiLuJe](https://www.mobileread.com/forums/showthread.php?t=225030) |
| koreader-kindle-v2026.07.1.zip | v2026.07.1 | AGPL-3.0 | [koreader/koreader](https://github.com/koreader/koreader) |
| fr-fr.tar.zst, en-fr.tar.zst | version 20261016 | GPL-3.0 (outil), CC BY-SA (données Wiktionnaire) | [xxyzz/wiktionary_stardict](https://github.com/xxyzz/wiktionary_stardict) |

Ces fichiers ne sont pas versionnés : `scripts/fetch-files.sh` les télécharge à la source et vérifie leurs empreintes. Tout le mérite revient à leurs auteurs : NiLuJe et la communauté MobileRead, KindleModding, et l'équipe KOReader.

## Avertissement

Un jailbreak modifie le système de l'appareil. Le risque est faible avec cette méthode, mais pas nul. Faites-le sur un appareil qui vous appartient. Rien ici ne contourne les DRM : KOReader n'ouvre que les livres sans DRM.
