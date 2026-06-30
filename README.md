# wingspan-assets

Generic stackable-token resource icons for Wingspan-style Tabletop
Simulator mods. Originally cut from the
[tabletop-mods](https://github.com/afermg/tabletop-mods) repo so the
generated PNGs can be served from a public URL that TTS can fetch at
runtime.

All icons are simple geometric primitives (colored circles + symbolic
shapes) — functional resource indicators, not reproductions of
commercial token artwork.

## Layout

```
wingspan-assets/
├── flake.nix             # reproducible build (python3 + librsvg)
├── scripts/
│   └── gen_resource_icons.py
└── icons/
    ├── invertebrate.{svg,png}
    ├── seed.{svg,png}
    ├── fish.{svg,png}
    ├── fruit.{svg,png}
    ├── rodent.{svg,png}
    └── nectar.{svg,png}
```

## Build

```sh
nix build .#icons
# -> ./result/svg/*.svg  +  ./result/png/*.png
```

Or directly:

```sh
nix-shell -p python3 librsvg
python3 scripts/gen_resource_icons.py
for f in icons/*.svg; do
  rsvg-convert -w 256 -h 256 "$f" -o "icons/$(basename "$f" .svg).png"
done
```

## Using from TTS

PNGs are served via `raw.githubusercontent.com`:

```
https://raw.githubusercontent.com/afermg/wingspan-assets/master/icons/<kind>.png
```

Pass any of those URLs to a `Custom_Token` / `Custom_Tile` spawn for the
token face.

## License

MIT — see `LICENSE`. The icons are original generic shapes; do not
infer trademark or association with any commercial board game.
