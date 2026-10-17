# files/

Third-party files used by the guide. They are **not committed**: run

```sh
./scripts/fetch-files.sh            # everything (~160 MB)
./scripts/fetch-files.sh --no-dict  # without the dictionaries
```

The script downloads each file from its upstream at the exact version tested, checks its SHA-256, and extracts `KUAL-KDK-1.0.azw2` from the KUAL archive.

| File | SHA-256 |
|---|---|
| K4-Jailbreak.zip | `b6e22bcf538ee474d7097fcd75969f1a7b2e9f226ec49fb587922d825a454dbb` |
| KUAL-v2.7.37-gfcb45b5-20250419.tar.xz | `40c4b68712213adc7b667b9502cdd0c8099761fce1e1bf2b161b84102af54135` |
| KUAL-KDK-1.0.azw2 (extracted) | `70c301f255bbad181c281aa7bf9ef89364ae9fe26ca527d8139ce6e3a283e140` |
| koreader-kindle-v2026.07.1.zip | `1fa9cc2784ffa42eaa309445d4e81661f825614c9c32349554fed6e4c8757a1d` |
| fr-fr.tar.zst | `c372aba291ea4558cfcd2efa2a5d54cfe97fc152b9ccd164113f9789a0018a79` |
| en-fr.tar.zst | `cf48dedd8ebe0426a5d9df6bc63256d757dd44bcdb9f4cc9935fc0124c524283` |
