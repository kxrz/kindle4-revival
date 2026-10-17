#!/bin/sh
# Dump the framebuffer to /mnt/us/screenshots after a delay, so there is
# time to leave KUAL and open the screen you want to capture.
# Convert on a computer with raw2png.py.
DELAY="${1:-10}"
OUT=/mnt/us/screenshots
(
	sleep "$DELAY"
	mkdir -p "$OUT"
	NAME="$OUT/$(date +%Y%m%d-%H%M%S)"
	FB=/sys/class/graphics/fb0
	{
		echo "virtual_size=$(cat $FB/virtual_size 2>/dev/null)"
		echo "bits_per_pixel=$(cat $FB/bits_per_pixel 2>/dev/null)"
		echo "stride=$(cat $FB/stride 2>/dev/null)"
		echo "modes=$(head -1 $FB/modes 2>/dev/null)"
	} > "$NAME.info"
	cat /dev/fb0 > "$NAME.raw"
	sync
) > /dev/null 2>&1 &
