#!/usr/bin/env python
"""Standalone entry point for the Jaon compiler executable."""
import sys

from jaon.cli import main

if __name__ == "__main__":
    sys.exit(main())
