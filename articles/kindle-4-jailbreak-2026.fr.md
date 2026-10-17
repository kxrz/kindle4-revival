# Jailbreaker une Kindle 4 en 2026 : le guide qui marche vraiment

Ma Kindle 4 a quinze ans. Plus de garantie, plus de mises à jour, et une interface qui commençait à ressembler à un musée. Elle méritait mieux qu'un tiroir.

Le problème, c'est que la plupart des tutoriels qu'on trouve en ligne sont périmés. Certains décrivent des outils pour d'autres modèles. D'autres ignorent un changement survenu en avril 2025 qui casse silencieusement tout l'écosystème. On suit les étapes, on obtient un message d'erreur obscur, et on abandonne.

Ce guide raconte ce qui fonctionne en octobre 2026, pièges compris. Tous les fichiers nécessaires sont dans le dossier [`files/`](../files/) du dépôt, aux versions exactes que j'ai testées, et les scripts dans [`tools/`](../tools/).

> Un tutoriel de jailbreak a la durée de vie d'un yaourt. Celui-ci est daté : octobre 2026.

---

## Ce qu'on va obtenir

- **KOReader**, un lecteur libre bien plus riche que celui d'Amazon : EPUB natif, typographie fine, césure française, statistiques de lecture, notes exportables.
- **Des dictionnaires hors ligne** en français.
- **Une bibliothèque rangée** par genre, auteur et série, lisible avec le pavé directionnel.
- L'interface Amazon reste intacte. On ajoute, on ne remplace pas.

**Avertissement** : un jailbreak modifie le système de l'appareil. Le risque de rendre la liseuse inutilisable est faible avec cette méthode, mais il n'est pas nul. Faites-le sur un appareil qui vous appartient.

---

## 0. Récupérer les fichiers

Depuis le dépôt, un script télécharge tout et vérifie les empreintes SHA-256 :

![Téléchargement des fichiers](../docs/img/01-fetch-files.svg)

| Fichier | Rôle | Source |
|---|---|---|
| `K4-Jailbreak.zip` | le jailbreak (v1.0.0, juin 2026) | [KindleModding](https://github.com/KindleModding/K4-Jailbreak) |
| `KUAL-KDK-1.0.azw2` | le lanceur d'extensions (v2.7.37) | [MobileRead](https://www.mobileread.com/forums/showthread.php?t=225030) |
| `koreader-kindle-v2026.07.1.zip` | le lecteur | [KOReader](https://github.com/koreader/koreader/releases) |
| `fr-fr.tar.zst`, `en-fr.tar.zst` | dictionnaires Wiktionnaire | [wiktionary_stardict](https://github.com/xxyzz/wiktionary_stardict) |

---

## 1. Identifier sa Kindle (l'étape que tout le monde saute)

C'est là que j'ai perdu le plus de temps. Ma première tentative utilisait **WinterBreak**, le jailbreak à la mode depuis fin 2024. Il est excellent… pour les Kindle récentes en firmware 5.x. Sur une Kindle 4, il ne sert strictement à rien.

Vérifiez deux choses :

1. **Le firmware** : `Menu → Paramètres`, la version s'affiche en bas de l'écran. Une Kindle 4 est en **4.x**, la dernière version étant **4.1.4** (2019).
2. **Le numéro de série** : `Menu → Paramètres → Menu → Infos sur l'appareil`. Une Kindle 4 sans écran tactile commence par **B00E** (modèle argenté, 2011) ou **B023** (modèle noir, 2012).

Si votre firmware commence par 5, ce guide n'est pas pour vous : allez voir [kindlemodding.org](https://kindlemodding.org/).

Bonne nouvelle pour les Kindle 4 : Amazon ne publiera plus de mise à jour. Le jailbreak ne sera jamais effacé par une mise à jour automatique.

---

## 2. Le piège de 2025 : les certificats expirés

En avril 2025, les certificats de développeur utilisés par toute la communauté ont expiré. Concrètement, KUAL refuse de s'ouvrir avec ce message :

> « Cet appareil n'est pas autorisé en tant que Kindle de test par le développeur de cet élément. »

Les anciens paquets de jailbreak installent les anciens certificats. NiLuJe, mainteneur historique des outils Kindle sur MobileRead, a publié des certificats renouvelés (*DevCerts-20250419*), et KUAL a été recompilé avec (version 2.7.37).

La solution la plus simple aujourd'hui : le paquet **K4-Jailbreak v1.0.0** de KindleModding (juin 2026), qui embarque directement les nouveaux certificats. J'ai ouvert son `data.tar.gz` avant de m'en servir : le magasin de clés installé contient des certificats valides jusqu'en 2099.

---

## 3. Le jailbreak

1. Passez la Kindle en **mode avion**.
2. Décompressez `K4-Jailbreak.zip` et copiez à la **racine** de la Kindle `data.tar.gz`, `ENABLE_DIAGS` et le dossier `diagnostic_logs` :

![Copie des fichiers du jailbreak](../docs/img/02-copy-jailbreak.svg)

3. Débranchez la Kindle, puis `Menu → Paramètres → Menu → Redémarrer`.
4. Elle démarre sur un écran texte de **diagnostic**. Avec le pavé directionnel :
   - `D) Exit, Reboot or Disable Diags`
   - `R) Reboot System`
   - puis la touche **gauche** du pavé pour confirmer.
5. Une image de jailbreak s'affiche avec une petite animation pendant une dizaine de secondes, puis la Kindle redémarre seule.

Un document **« You are Jailbroken »** apparaît dans la bibliothèque. C'est fait.

Gardez `Update_jailbreak_1.8.N_uninstall.bin` (dans le zip) : c'est le désinstalleur.

---

## 4. Installer KUAL

Sur une Kindle 4, KUAL n'est pas un paquet à installer : c'est un simple document. Copiez `KUAL-KDK-1.0.azw2` dans le dossier `documents` de la Kindle, éjectez, et ouvrez **KUAL** depuis la bibliothèque comme un livre.

**Attention** : n'utilisez **ni** `KUAL-KDK-2.0.azw2` (Kindle Touch et suivantes) **ni** les paquets `Update_KUALBooklet_*.bin` (Kindle récentes). C'est le deuxième piège, et il est vicieux.

---

## 5. Si KUAL plante avec une « RuntimeException »

C'est le message que j'ai obtenu une fois les certificats réglés :

> « Une erreur s'est produite : l'instanciation de la classe principale (Main) a levé une exception de type RuntimeException. »

Les forums MobileRead attribuent ce message à une version **Booklet** de KUAL installée par erreur. C'est exact, mais la solution proposée (lancer `Update_KUALBooklet_*_uninstall.bin` via « Mettre à jour votre Kindle ») ne s'applique pas à une Kindle 4 : j'ai inspecté ce paquet, il ne cible que les identifiants des Kindle 5. La Kindle 4 le refuse.

### Diagnostiquer

KUAL écrit son propre journal d'erreur sur le stockage USB, dans `developer/KUAL/work/crash.log` :

![Le journal d'erreur de KUAL](../docs/img/03-kual-crash-log.svg)

`javax.swing.JButton` est la clé. Swing est la bibliothèque graphique des Kindle Touch. KUAL croit tourner sur une Touch.

### Trouver le coupable

Le README officiel du jailbreak le précise : s'il trouve un fichier `runme.sh` à la racine, il l'exécute en root à la fin. J'ai écrit un script de diagnostic en lecture seule ([`tools/diagnostic/runme.sh`](../tools/diagnostic/runme.sh)) qui dresse l'état du système dans `diag/report.txt` :

![Le rapport de diagnostic](../docs/img/04-diag-report.svg)

Le voilà. Un `KUALBooklet.jar` daté du 27 juillet 2023, déposé par ma propre tentative ratée de l'époque (avec un vieux MRPI). Le système charge ce dossier au démarrage, et le jailbreak Java donne la priorité aux classes système. La version Kindle 4 de KUAL se fait doubler par la version Kindle 5.

> Les restes d'une installation ratée sont parfois plus dangereux que l'installation elle-même.

### La correction

Même mécanisme, avec [`tools/fix-kual-booklet/runme.sh`](../tools/fix-kual-booklet/runme.sh), qui sauvegarde puis supprime le fichier :

![Application du correctif](../docs/img/05-fix-kual-booklet.svg)

KUAL s'ouvre au premier essai. Le script laisse une copie du fichier supprimé (`KUALBooklet.jar.bak`) et un compte rendu (`fix-kual-booklet.log`) à la racine de la Kindle.

---

## 6. Installer KOReader

Le paquet à prendre est **`koreader-kindle`**. Le nom est trompeur : `kindle-legacy` vise les modèles à clavier (Kindle 2, DX, 3), `kindlepw2` et `kindlehf` les modèles récents.

![Installation de KOReader](../docs/img/06-install-koreader.svg)

Ouvrez KUAL : un menu **KOReader** est apparu. Deux façons de le lancer :

- **Start KOReader** : rapide, l'interface Amazon reste chargée en arrière-plan.
- **Start KOReader (no framework)** : coupe l'interface Amazon et libère de la mémoire. Sur une machine de 2011, c'est le mode que je recommande. Au retour, la Kindle relance son interface en une trentaine de secondes.

Deux règles :

- **Quittez KOReader avant de brancher la Kindle en USB.** Tant qu'il tourne, la Kindle ne se monte pas.
- Les mises à jour de KOReader se font ensuite depuis KOReader lui-même, Wi-Fi activé, avec l'option « Mettre à jour » de son menu.

---

## 7. Dictionnaires français

KOReader lit les dictionnaires StarDict placés dans `koreader/data/dict/`, **un sous-dossier par dictionnaire**. Sinon, les fichiers communs comme `res/` s'écrasent mutuellement (je l'ai appris à mes dépens).

J'utilise le **Wiktionnaire français-français** (545 000 entrées) et le **Wiktionnaire anglais-français** pour les livres en VO :

![Installation des dictionnaires](../docs/img/07-dictionaries.svg)

Pour chercher un mot sans écran tactile : dans un livre, appuyez sur la touche clavier ou sur le bouton central pour faire apparaître le curseur, déplacez-le avec le pavé, puis validez. La première recherche est lente (chargement de l'index). Les suivantes sont instantanées.

---

## 8. Organiser sa bibliothèque

J'avais environ 680 EPUB éparpillés dans huit dossiers : des collections thématiques et des lots récupérés au fil des années. Copiés tels quels, ils auraient donné une liste ingérable sur un écran de 600 × 800 sans tactile.

### Le principe

KOReader a son propre navigateur de fichiers. Les collections Amazon ne lui servent à rien, ce sont les **dossiers** qui comptent. J'ai retenu trois niveaux :

```
documents/
├── Essais & documents/
├── Fantastique & fantasy/
├── Jeunesse/
├── Littérature/
├── Polar & thriller/
└── Science-fiction/
    └── Herbert, Frank/
        ├── Dune 01 - Dune.epub
        ├── Dune 03 - Les enfants de Dune.epub
        └── Les yeux d'Heisenberg.epub
```

- **Le genre** d'abord, parce qu'on choisit rarement un livre par auteur un soir de fatigue.
- **L'auteur** au format `Nom, Prénom`, pour un tri alphabétique correct.
- **La série et son numéro** en tête du nom de fichier, pour que les tomes s'affichent dans l'ordre.

Deux clics pour arriver à un auteur. C'est le bon compromis avec un pavé directionnel.

### Le vrai problème : les métadonnées

Les fichiers récupérés ici et là ont des métadonnées dans un état lamentable. Le même auteur apparaissait sous trois formes (« Lee Child », « Child, Lee », « Child »). Des titres traînaient des « (French Edition) », des noms de sites, des années. Une dizaine de livres avaient même le titre et l'auteur inversés.

J'ai écrit [`tools/organize-library/organize_library.py`](../tools/organize-library/), sans dépendance, qui lit les métadonnées de chaque EPUB, normalise les auteurs, nettoie les titres, récupère les séries, devine le genre et écarte les doublons. Il ne touche jamais aux originaux, et par défaut il se contente d'afficher ce qu'il ferait :

![Classement d'une bibliothèque](../docs/img/08-organize-library.svg)

Un petit fichier JSON permet de corriger ce que l'automatique rate : genre d'un auteur, variante de nom, titre récalcitrant. Quand le plan convient, on relance avec `--apply`.

Sur ma bibliothèque : 645 livres, 31 doublons écartés, 432 Mo. Ça tient dans le giga libre de la Kindle 4.

### Le réglage qui change tout

Par défaut, KOReader n'affiche pas le nom des fichiers mais le titre inscrit dans les métadonnées. Tout le travail de nettoyage serait invisible. Dans le navigateur de fichiers, menu « Mode d'affichage », choisissez :

- « Liste détaillée avec les images de couverture et les noms de fichiers », ou
- « Classique (nom du fichier seulement) », plus rapide sur ce vieux processeur.

Le premier affichage avec couvertures est lent, le temps de les générer. Elles sont ensuite gardées en cache.

**À propos des DRM** : KOReader ne lit pas les livres protégés. Un `META-INF/encryption.xml` dans un EPUB ne veut pas forcément dire DRM. Dans trois de mes fichiers, il ne chiffrait que les polices intégrées (une obfuscation Adobe), et le livre s'ouvre normalement.

---

## 9. Réglages utiles

- **Langue** : option « Language » du menu (elle devient « Langue » une fois le français choisi).
- **Rafraîchissement complet** toutes les 6 pages, contre la rémanence de l'encre électronique : option « Fréquence des rafraîchissements complets (flash noir) ».
- **Wi-Fi coupé automatiquement** : menu « Réseau », option « Auto-disable Wi-Fi » (pas encore traduite).
- **Police** : *Noto Serif* est très lisible sur cet écran 167 ppp. On peut ajouter ses propres polices `.ttf` dans `koreader/fonts/`.
- **Valeurs par défaut** : un appui long sur un réglage typographique (taille, marges, interligne) le définit pour tous les livres.

---

## 10. Envoyer des livres sans câble

KOReader intègre un connecteur **Calibre** :

1. Dans Calibre (sur l'ordinateur) : bouton « Connecter/partager », puis l'option de connexion sans fil à un appareil.
2. Dans KOReader, Wi-Fi activé, sur le même réseau : menu « Calibre », puis « Calibre wireless connect ».
3. Envoyez les livres depuis Calibre comme vers n'importe quelle liseuse.

---

## Récapitulatif des pièges

| Symptôme | Cause | Solution |
|---|---|---|
| WinterBreak ne fait rien | Outil pour Kindle 5.x | K4-Jailbreak |
| « Pas autorisé en tant que Kindle de test » | Certificats de 2025 absents | K4-Jailbreak v1.0.0 |
| « RuntimeException », `javax.swing.JButton` dans `crash.log` | `KUALBooklet.jar` dans le système | [`tools/fix-kual-booklet`](../tools/fix-kual-booklet/runme.sh) |
| La Kindle ne se monte pas en USB | KOReader tourne encore | Quitter KOReader avant de brancher |
| KOReader ne démarre pas | Mauvais paquet | `kindle`, pas `kindle-legacy` |
| Titres illisibles dans KOReader | Affichage des métadonnées | Mode d'affichage « noms de fichiers » |

---

## Sources

- [KindleModding : jailbreak Kindle 4](https://kindlemodding.org/jailbreaking/Legacy/K4-Jailbreak/)
- [KindleModding : KUAL et MRPI](https://kindlemodding.org/jailbreaking/Legacy/post-jailbreak/installing-kual-mrpi/)
- [MobileRead : snapshots des outils de NiLuJe](https://www.mobileread.com/forums/showthread.php?t=225030)
- [MobileRead : DevCerts 2025](https://www.mobileread.com/forums/showpost.php?p=4506164)
- [MobileRead : K4 FW 4.1.4, problèmes KUAL/MRPI](https://www.mobileread.com/forums/showthread.php?t=367615)
- [KOReader : installation sur Kindle](https://github.com/koreader/koreader/wiki/Installation-on-Kindle-devices)
- [Dictionnaires Wiktionary au format StarDict](https://github.com/xxyzz/wiktionary_stardict)

Une liseuse de 2011 qui lit mieux l'EPUB que bien des appareils neufs, ce n'est pas de la nostalgie. C'est juste du logiciel bien fait sur du matériel qui n'avait aucune raison de mourir.
