#!/usr/bin/env python3

from bdsim import bdrun
import sys

print(sys.argv)

bdrun(sys.argv[-1], sysargs=True)
