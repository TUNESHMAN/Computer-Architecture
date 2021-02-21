#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *


# take in some value
if len(sys.argv) != 2:
    print(f"usage:{sys.argv[0]} <filename>")
    sys.exit(1)


cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()
