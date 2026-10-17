# fix-kual-booklet

**Symptom** (Kindle 4, firmware 4.x): KUAL opens with *"Main class instantiation threw a RuntimeException"*, and `developer/KUAL/work/crash.log` contains `java.lang.NoClassDefFoundError: javax.swing.JButton`.

**Cause**: a `KUALBooklet.jar` (the Kindle 5 build of KUAL) sits in `/opt/amazon/ebook/booklet/`, usually left by an earlier attempt with MRPI. The system loads it first. The official `Update_KUALBooklet_*_uninstall.bin` only targets Kindle 5 device IDs, so a Kindle 4 refuses it.

**Fix**: copy `runme.sh` to the root of the Kindle drive with the K4 jailbreak files (`data.tar.gz`, `ENABLE_DIAGS`, `diagnostic_logs/`), run the jailbreak again (Restart, then D → R → left), and delete `runme.sh` afterwards. The script backs the jar up to `KUALBooklet.jar.bak` and writes `fix-kual-booklet.log` at the root of the drive.
