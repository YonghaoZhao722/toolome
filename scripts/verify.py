"""DEPRECATED. The old version rewrote src/data/tools.json from candidates.py and destroyed data.
This file is now a read-only link checker kept only for backwards compatibility.
Use `python3 scripts/audit.py [--online]` instead. It never writes tools.json unless --fix is passed."""
import subprocess,sys
sys.exit(subprocess.call([sys.executable,"scripts/audit.py","--online","--links"]))
