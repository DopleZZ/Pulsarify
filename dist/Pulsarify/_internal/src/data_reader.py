import csv
import os
import sys
from typing import Optional


def get_data_dir() -> str:
    """Return path to data directory.

    When bundled with PyInstaller the files are placed under sys._MEIPASS.
    Otherwise fall back to local 'data' directory next to the project root.
    """
    # If running in a PyInstaller bundle, _MEIPASS contains the extracted files
    base = getattr(sys, '_MEIPASS', None)
    if base:
        candidate = os.path.join(base, 'data')
        if os.path.isdir(candidate):
            return candidate

    # Fallback: look for data directory relative to this file (project layout)
    here = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.join(here, '..', 'data')
    candidate = os.path.normpath(candidate)
    if os.path.isdir(candidate):
        return candidate

    # Last resort: a 'data' in cwd
    cwd_candidate = os.path.join(os.getcwd(), 'data')
    if os.path.isdir(cwd_candidate):
        return cwd_candidate

    # If none found, return the path where we expect it (caller will handle missing file)
    return candidate


def read_z_values() -> list[float]:
    z_values = []
    data_dir = get_data_dir()
    path = os.path.join(data_dir, 'cp1919.csv')
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            z_values.append(float(row['z']))
    return z_values


def read_text() -> str:
    data_dir = get_data_dir()
    path = os.path.join(data_dir, 'input.txt')
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def get_output_dir() -> str:
    """Return a writable output directory.

    If the current working directory is writable, use it. If the app is
    running from a bundled location (sys._MEIPASS) or cwd is not writable,
    return the user's Downloads directory so saving does not fail on a
    read-only mounted DMG.
    """
    # prefer cwd if writable
    try:
        cwd = os.getcwd()
        test_file = os.path.join(cwd, '.pulsarify_write_test')
        with open(test_file, 'w') as f:
            f.write('x')
        os.remove(test_file)
        return cwd
    except Exception:
        # fallback to Downloads
        dl = os.path.expanduser(os.path.join('~', 'Downloads'))
        try:
            os.makedirs(dl, exist_ok=True)
        except Exception:
            dl = os.path.expanduser('~')
        return dl