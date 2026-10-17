# kual-screenshot

A tiny KUAL extension that dumps the Kindle framebuffer after a delay, so you have time to leave KUAL and open the screen you want, plus a converter to PNG. The KOReader screenshot in this repository was made with it.

1. Copy `extensions/screenshot/` into the `extensions/` folder of the Kindle.
2. KUAL → Screenshot → *Capture in 10 seconds* (or 30), then go to the screen to capture and wait.
3. Plug the Kindle in and convert:

```sh
python3 raw2png.py /Volumes/Kindle/screenshots/*.raw --out docs/img/
```

Each capture is a `.raw` dump plus a `.info` file (resolution, bits per pixel, line length). On the Kindle 4 the framebuffer is 600 × 800, 8 bpp, and stored inverted; the converter detects that and flips it. Force it with `--invert` / `--no-invert`.

Don't script repeated KOReader launches around it: I tried an automated tour (open KOReader, capture, quit, three times in a row with KUAL still open) and the Amazon framework crashed on the way back. One capture at a time is fine.
