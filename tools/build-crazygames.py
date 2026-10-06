#!/usr/bin/env python3
"""Kept for older notes — same as `python3 tools/build.py crazygames`."""
import os, subprocess, sys
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'build.py'), 'crazygames'], check=True)
