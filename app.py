#!/usr/bin/env python3
import sys
import os


base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(base_dir, 'src')
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    
    from src.gui import run_app
except Exception as e:
    
    print('Failed to import application modules:', e)
    raise


def main():
    run_app()


if __name__ == '__main__':
    main()
