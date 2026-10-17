#!/bin/sh
# Kindle 4 (firmware 4.x): read-only system report.
#
# Run it the same way as fix-kual-booklet: copy it as runme.sh to the root of
# the Kindle drive with the jailbreak files, run the jailbreak, then read
# diag/report.txt on the drive. Nothing is modified on the device.

OUT=/mnt/us/diag
mkdir -p $OUT
exec > $OUT/report.txt 2>&1
R=/var/tmp/diagroot
mkdir -p $R
mount -o ro /dev/mmcblk0p1 $R

echo "== firmware"; cat $R/etc/prettyversion.txt
echo "== java libraries"; ls -la $R/opt/amazon/ebook/lib/
md5sum $R/opt/amazon/ebook/lib/json_simple-1.1.jar
echo "== booklets (KUALBooklet.jar must NOT be here on a Kindle 4)"; ls -la $R/opt/amazon/ebook/booklet/
echo "== update keys"; ls -la $R/etc/uks/
echo "== developer keystore"; ls -la /var/local/java/keystore/
md5sum /var/local/java/keystore/developer.keystore
echo "== hacks found in the system partition"
find $R -xdev \( -iname '*kual*' -o -iname '*launchpad*' -o -iname '*mrpi*' -o -iname '*mkk*' \) 2>/dev/null

mkdir -p $OUT/logs
cp -a /var/local/log/* $OUT/logs/ 2>/dev/null
umount $R
sync
