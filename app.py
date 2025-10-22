#!/usr/bin/env python3
"""Launcher for PyInstaller bundling.

This script makes sure `src/` is on sys.path both in development and in a PyInstaller
frozen bundle (uses sys._MEIPASS). It then imports and runs the GUI entrypoint.
"""
import sys
import os

# Resolve base directory: in frozen apps PyInstaller extracts into _MEIPASS
base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(base_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    # import the GUI entrypoint defined in src/gui.py (use package import)
    from src.gui import run_app
except Exception as e:
    # Provide a helpful error when imports fail
    print('Failed to import application modules:', e)
    raise


def main():
    run_app()


if __name__ == '__main__':
    main()
