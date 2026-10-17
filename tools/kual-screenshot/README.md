# kual-screenshot

A tiny KUAL extension that dumps the Kindle framebuffer after a delay, so you have time to leave KUAL and open the screen you want, plus a converter to PNG.

1. Copy `extensions/screenshot/` into the `extensions/` folder of the Kindle.
2. KUAL → Screenshot → *Capture in 10 seconds* (or 30), then go to the screen to capture and wait.
3. Plug the Kindle in and convert:

```sh
python3 raw2png.py /Volumes/Kindle/screenshots/*.raw --out docs/img/
```

Each capture is a `.raw` dump plus a `.info` file (resolution, bits per pixel, line length). The converter handles 8 and 4 bpp grayscale and inverts the image automatically when it comes out mostly dark. Force it with `--invert` / `--no-invert`.
