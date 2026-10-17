#!/bin/sh
# Screenshot tour used to illustrate the guide. Started from KUAL, it captures
# the KUAL menu, then opens KOReader on a few locations and captures each one.
# Edit the paths below for your own library.
OUT=/mnt/us/screenshots
KO=/mnt/us/koreader/koreader.sh
DOC=/mnt/us/documents
LOG=$OUT/tour.log
(
	mkdir -p $OUT
	shot() {
		FB=/sys/class/graphics/fb0
		{
			echo "virtual_size=$(cat $FB/virtual_size)"
			echo "bits_per_pixel=$(cat $FB/bits_per_pixel)"
			echo "stride=$(cat $FB/stride)"
			echo "modes=$(head -1 $FB/modes)"
		} > "$OUT/$1.info"
		cat /dev/fb0 > "$OUT/$1.raw"
		sync
		echo "$(date) shot $1" >> $LOG
	}
	# ko NAME PATH SECONDS: open PATH in KOReader, wait, capture, quit
	ko() {
		echo "$(date) open $2" >> $LOG
		$KO --kual "$2" >> $LOG 2>&1 &
		KPID=$!
		sleep "$3"
		shot "$1"
		killall -TERM reader.lua 2>/dev/null
		i=0
		while kill -0 $KPID 2>/dev/null && [ $i -lt 90 ]; do sleep 1; i=$((i+1)); done
		sleep 5
	}
	echo "$(date) tour start" > $LOG
	sleep 3
	shot 01-kual-menu
	ko 02-koreader-home "$DOC" 45
	ko 03-koreader-author "$DOC/Science-fiction/Verne, Jules" 60
	ko 04-koreader-reading "$DOC/Science-fiction/Verne, Jules/Le tour du monde en quatre-vingts jours.epub" 60
	echo "$(date) tour done" >> $LOG
) > /dev/null 2>&1 &
