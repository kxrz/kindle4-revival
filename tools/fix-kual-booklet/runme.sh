#!/bin/sh
# Kindle 4 (firmware 4.x): remove a KUAL Booklet left in the system partition.
#
# KUALBooklet.jar is the Kindle 5 build of KUAL. If an earlier attempt put it
# in /opt/amazon/ebook/booklet/, the system loads it first and the Kindle 4
# build of KUAL crashes with "Main class instantiation threw a RuntimeException"
# (crash.log: java.lang.NoClassDefFoundError: javax.swing.JButton).
#
# How to run: copy this file to the root of the Kindle drive together with the
# K4 jailbreak files (data.tar.gz, ENABLE_DIAGS, diagnostic_logs) and run the
# jailbreak again. The jailbreak executes /mnt/us/runme.sh as root at the end.
# Delete runme.sh afterwards. A backup of the jar is kept at the drive root.

R=/var/tmp/rootfs_fix
JAR=$R/opt/amazon/ebook/booklet/KUALBooklet.jar
LOG=/mnt/us/fix-kual-booklet.log
mkdir -p $R
mount -o rw /dev/mmcblk0p1 $R || { echo "mount failed" > $LOG; exit 0; }
if [ -f "$JAR" ] ; then
	cp -a "$JAR" /mnt/us/KUALBooklet.jar.bak
	chattr -i "$JAR" 2>/dev/null
	rm -f "$JAR"
	echo "KUALBooklet.jar removed (backup: KUALBooklet.jar.bak)" > $LOG
else
	echo "KUALBooklet.jar not found, nothing to do" > $LOG
fi
ls -la $R/opt/amazon/ebook/booklet/ >> $LOG
sync
umount $R
sync
