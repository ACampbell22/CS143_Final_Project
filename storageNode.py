#!/usr/bin/env python

import file_ecc
from node import Node

class StorageNode(Node):
    """Extension of the Node class to provide an erasure code based storage
       mechanism. Uses a 20/10 erasure code internally. This could be generalized
       to an n/k code by passing the proper parameters, however, we hard code 20/10
       for simplicity, since this mainly serves as a proof-of-concept."""
    def __init__(self, address):
        super(StorageNode, self).__init__(address)

    def add_key(self, key, val):
        key_ident = self.hash_key(key)
        node = self.find_successor(key_ident)

        if int(node['ident']) == self.ident:
            self.keys[key] = val
            addr = self.address
            return {'node': addr, 'status': 'Added'}
        else:
            print 'Sending to remote %s' % node['address']
            return remote_call(node['address'], 'add_key', [key, val])

    def storeFile(self, filePath):
        prefix = '/tmp/' + self.ident() + '_' + filePath.split('/')[-1]
        fileBlocks = file_ecc.EncodeFile(filePath, prefix, 20, 10)
        for block in fileBlocks:
            self.add_key(block, block)

    def getFile(self, filePath):
        prefix = '/tmp/' + self.ident() + '_' + filePath.split('/')[-1]
        blockNames = []
        for i in xrange(20):
            blockNames.append(prefix + ".p_" + i)
        file_ecc.DecodeFiles(blockNames, prefix + ".r")

def main():
    node = StorageNode('127.0.0.1:2000')
    node._ident = 1000
    print "Joining"
    node.join()
    print "Running node"
    node.run()

if __name__ == '__main__':
    main()
