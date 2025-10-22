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

Codesigning & notarization (high level)
- Codesign your app:

```bash
codesign --deep --force --verbose --sign "Developer ID Application: Your Name (TEAMID)" dist/Pulsarify.app
```

- Create an unsigned ZIP and upload for notarization, or use altool/xcrun notarytool per Apple's docs.

After notarization is approved, staple the ticket:

```bash
xcrun stapler staple dist/Pulsarify.app
```

Troubleshooting
---------------
- If the app crashes at startup in a bundled state, run the binary with stdout/stderr captured or run the executable inside `dist/Pulsarify.app/Contents/MacOS/Pulsarify` from Terminal to see error traces.
- GUI requires macOS system frameworks — build must be performed on macOS to get a valid `.app` / `.dmg`.

If you want, I can: add a packaged icon, add exclusion rules for PyInstaller, or refine the PyInstaller spec to include fonts explicitly and reduce bundle size.
