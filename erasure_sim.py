#!/usr/bin/env python2.7
"""
CS143 Final Project
Simulation of Erasure Code Performance in Unreliable Mobile Networks

Jeff Rogers
Nicolai Astrup Wiik
Andrew Campbell
Dawit Gebregziabher
"""

import random
import genericmatrix
import math
import ffield
from storageNode import StorageNode
import subprocess
import time

import zerorpc

def main():
    # print "Setting up network"
    # First we setup the network. We'll use 7 nodes, but more can be added as desired
    # local = "127.0.0.1:"
    # port = 2000
    # for i in xrange(0,7):
    #     subprocess.Popen(["./join.py", local + str(port + i), local + str(port)])
    #     print "."
    #     time.sleep(1)

    # print "Storing files"
    ## Now we store a few files among nodes
    # for f in ["/ls", "/bin/date", "/bin/echo"]:
    #     client = zerorpc.Client()
    #     client.connect("tcp://%s" % (local + str(port + i)))
    #     client(storeFile, f)
    #     client.close()

    # print "Recovering files"
    ## Now we recover the files from the nodes
    # for f in ["/ls", "/bin/date", "/bin/echo"]:
    #     client = zerorpc.Client()
    #     client.connect("tcp://%s" % (local + str(port + i)))
    #     client(getFile, f)
    #     client.close()
    # print "Successfully recovered files\n"

    # Rather than running the simulation on our chord network, (which adds the complexity
    # of adding nodes to and taking nodes out of the network at random), we simulate the
    # performance of an erasure code based network under unreliable, mobile conditions
    # and a more typical, replication based system to compare performance. We measure
    # performance for several levels on unreliability, as given by a parameter to the
    # simulation function.
    print "Now simulating erasure code based network and replication based network for comparison"
    # Erase file if it already existed from a prior run
    f = open('results.txt', 'w')
    f.close()
    for redundancy in [2, 4, 8, 16]:
        for reliability in [0.01, 0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.99]:
            runSimulation(redundancy, reliability)
    print "Simulation completed. Check 'results.txt' for results of comparison"

## Function definitions

# Takes a single floating point value between 0 and 1 that indicates the reliability
# of an individual node. Runs
def runSimulation(redundancy, reliability):
    # Hard-coded values for 20/10 erasure code. We assume that the replication based
    # system uses a 2x replication strategy. We make the simplifying assumption that
    # files are always successfully stored with the proper number of nodes (i.e. that
    # with a 20/10 erasure code the file is always stored with 20 distinct nodes)
    n = 10 * redundancy
    k = 10
    rep = redundancy
    numNodes = 100
    numFiles = 100000

    erasureFails = 0
    for i in xrange(numFiles):
        count = 0
        for j in xrange(n):
            if random.random() <= reliability:
                count += 1
        if count < k:
            erasureFails += 1

    repFails = 0
    for i in xrange(numFiles):
        recovered = False
        for j in xrange(rep):
            if random.random() <= reliability:
                recovered = True
                break

        if not recovered:
            repFails += 1

    f = open('results.txt', 'a')
    f.write("Stored {0} files\n".format(numFiles))
    f.write("{0}x replication\n".format(rep))
    f.write("{0}/{1} erasure code\n".format(n, k))
    f.write("Node reliability: {0}\n".format(reliability))
    f.write("Erasure coding availability: {0}\n".format(float(numFiles - erasureFails)/numFiles))
    f.write("Replication availability:    {0}\n".format(float(numFiles - repFails)/numFiles))
    f.write("\n")
    f.close()

if __name__ == '__main__':
    main()
