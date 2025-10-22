Pulsarify — packaging & macOS DMG build
=====================================

This repository contains a Python GUI app that generates PNG/SVG using custom font measurement and embedding.

Quick start (developer)
-----------------------
1. Create & activate virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the GUI:

```bash
python src/gui.py
```

Create an all-in-one macOS DMG (build machine must be macOS)
-----------------------------------------------------------------
This provides a conservative script to build using PyInstaller and package a DMG.

Usage:

```bash
chmod +x scripts/build_macos_dmg.sh
./scripts/build_macos_dmg.sh /absolute/path/to/output_dir
```

Notes and caveats
-----------------
- The build script creates a temporary virtualenv to avoid contaminating your system environment.
- The produced `.app` and `.dmg` are not codesigned or notarized. To distribute outside your machine you must codesign and notarize with Apple developer account.
