#!/bin/sh
# Download every third-party file used in the guide into files/,
# pinned to the exact versions tested, and verify their SHA-256.
# Usage: ./scripts/fetch-files.sh            (everything)
#        ./scripts/fetch-files.sh --no-dict  (skip the dictionaries, ~120 MB)
set -eu

cd "$(dirname "$0")/../files"

OVH="https://storage.gra.cloud.ovh.net/v1/AUTH_2ac4bfee353948ec8ea7fd1710574097/mr-public"
DICT="https://github.com/xxyzz/wiktionary_stardict/releases/download/20261016"

# name|url|sha256
FILES="
K4-Jailbreak.zip|https://github.com/KindleModding/K4-Jailbreak/releases/download/v1.0.0/K4-Jailbreak.zip|b6e22bcf538ee474d7097fcd75969f1a7b2e9f226ec49fb587922d825a454dbb
KUAL-v2.7.37-gfcb45b5-20250419.tar.xz|$OVH/KUAL/KUAL-v2.7.37-gfcb45b5-20250419.tar.xz|40c4b68712213adc7b667b9502cdd0c8099761fce1e1bf2b161b84102af54135
koreader-kindle-v2026.07.1.zip|https://github.com/koreader/koreader/releases/download/v2026.07.1/koreader-kindle-v2026.07.1.zip|1fa9cc2784ffa42eaa309445d4e81661f825614c9c32349554fed6e4c8757a1d
"
DICTS="
fr-fr.tar.zst|$DICT/fr-fr.tar.zst|c372aba291ea4558cfcd2efa2a5d54cfe97fc152b9ccd164113f9789a0018a79
en-fr.tar.zst|$DICT/en-fr.tar.zst|cf48dedd8ebe0426a5d9df6bc63256d757dd44bcdb9f4cc9935fc0124c524283
"
[ "${1:-}" = "--no-dict" ] || FILES="$FILES$DICTS"

echo "$FILES" | while IFS='|' read -r name url sum; do
	[ -n "$name" ] || continue
	if [ ! -f "$name" ]; then
		echo "Downloading $name"
		curl -fL --progress-bar -o "$name.part" "$url"
		mv "$name.part" "$name"
	fi
	if echo "$sum  $name" | shasum -a 256 -c - >/dev/null 2>&1; then
		echo "OK        $name"
	else
		echo "MISMATCH  $name (delete it and run again)" >&2
		exit 1
	fi
done

# KUAL for the Kindle 4 is the KDK-1.0 kindlet inside the archive
if [ ! -f KUAL-KDK-1.0.azw2 ]; then
	tar -xJf KUAL-v2.7.37-gfcb45b5-20250419.tar.xz KUAL-KDK-1.0.azw2
fi
echo "Done. Files are in $(pwd)"
