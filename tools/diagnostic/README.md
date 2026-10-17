# diagnostic

Read-only system report for a jailbroken Kindle 4. Copy `runme.sh` to the root of the Kindle drive together with the K4 jailbreak files and run the jailbreak again: it executes `runme.sh` as root at the end (this is documented in the jailbreak's README). The report lands in `diag/report.txt` on the drive. Delete `runme.sh` afterwards.

It lists the firmware, the Java libraries and booklets of the system partition, the update keys, the developer keystore, and any hack files found in the system partition. A `KUALBooklet.jar` in the booklets list is what breaks KUAL on a Kindle 4, see [`../fix-kual-booklet`](../fix-kual-booklet/runme.sh).
