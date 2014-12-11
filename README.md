# CS143 Final Project: Erasure Coding in Unreliable, Mobile P2P Networks

Group: Jeffrey Rogers, Andrew Campbell, Nico Astrup-Wiik, Dawit Gebregziabher

## Contents

This directory contains the source files for our final project.

The contents are as follows:
* 'ffield.py', 'file_ecc.py', 'rs_code.py', and 'genericmatrix.py' implement
  Reed-Solomon erasure coding. 'file_ecc.py' is imported by our StorageNode
  class and used to perform encoding and decoding on individual files. These
  files came from Emin Martinian and are available here:
  http://web.mit.edu/~emin/www.old/source_code/py_ecc/
* 'node.py' contains the implementation of a Chord network. It was modified
  from here: https://github.com/dash1291/chord
* 'storageNode.py' extends node.py to enable storage of erasure encoded files
* 'erasure_sim.py' sets up a small Chord network on the local machine (7 nodes,
  though this can be easily extended), stores files among the nodes, and then
  recovers them to demonstrate that the network works properly. Additionally,
  this file simulates both an erasure encoded storage system and a replication
  based storage system for a variety of redundancy and reliability levels.
  The results of these simulations are output to 'results.txt'
* 'join.py' is a helper that spawns processes in the background for erasure_sim.py
* 'results.txt' is output by erasure_sim.py. This output is discussed in our
  report.
* 'build.sh' is a simple shell script for testing and cleaning up any files
  produced by our tests.

## Running

First, note that you'll need zerorpc in order to run our code. This can easily
be installed via pip using `pip install zerorpc`.

Once zerorpc is installed, simply run `python erasure_sim.py`. This will setup
the chord network as described above and store and retrieve files to make sure
everything works properly. It also simulates an erasure code based P2P storage
network and a replication based storage system over a variety of redundancy and
reliablity levels, outputting the results into 'results.txt'