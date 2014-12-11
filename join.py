#!/usr/bin/env python2.7
"""Used by erasure_sim.py to join nodes as background processes"""

import sys
from storageNode import StorageNode

address = sys.argv[1]
connection = sys.argv[2]

node = StorageNode(address)

if len(sys.argv == 3):
    node.join(connection)
else:
    node.join()

node.run()
