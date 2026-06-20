#!/usr/bin/env python
"""Standalone entry point for the Helios compiler executable."""
import sys

from helios.cli import main

if __name__ == "__main__":
    sys.exit(main())
