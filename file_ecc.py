# Modified from Emin Martinian

__doc__ = """
This package implements an erasure correction code for files.
Specifically it lets you take a file F and break it into N
pieces (which are named F.p_0, F.p_1, ..., F.p_N-1) such that
F can be recovered from any K pieces.  Since the size of each
piece is F/K (plus some small header information).

How is this better than simply repeating copies of a file?

Firstly, this package lets you get finer grained
redunancy control since producing a duplicate copy of a file
requires at least 100% redundancy while this package lets you
expand the redunancy by n/k (e.g. if n=11, k=10 only 10%
redundancy is added).

Secondly, using a Reed-Solomon code as is done in this package,
allows better loss resistance.  For example, assume you just
divided a file F into 4 pieces, F.1, F.2, ..., F.4, duplicated
each piece and placed them each on a different disk.  If the
two disks containing a copy of F.1 go down then you can no longer
recover F.

With the Reed-Solomon code used in this package, if you use n=8, k=4
you divide F into 8 pieces such that as long as at least 4 pieces are
available recovery can occur.  Thus if you placed each piece on a
seprate disk, you could recover data as if any combination of 4 or
less disks fail.

The docstrings for the functions EncodeFile and DecodeFiles
provide detailed information on usage.

The following is an example of how to use this file:

>>> import file_ecc
>>> testFile = '/bin/ls'      # A reasonable size file for testing.
>>> prefix = '/tmp/ls_backup' # Prefix for shares of file.
>>> names = file_ecc.EncodeFile(testFile,prefix,15,11) # break into N=15 pieces

# Imagine that only pieces [0,1,5,4,13,8,9,10,11,12,14] are available.
>>> decList = map(lambda x: prefix + '.p_' + `x`,[0,1,5,4,13,8,9,10,11,12,14])

>>> decodedFile = '/tmp/ls.r' # Choose where we want reconstruction to go.
>>> file_ecc.DecodeFiles(decList,decodedFile)
>>> fd1 = open(testFile,'rb')
>>> fd2 = open(decodedFile,'rb')
>>> fd1.read() == fd2.read()
1
"""

from rs_code import RSCode
from array import array

import os, struct, string

headerSep = '|'

def GetFileSize(fname):
    return os.stat(fname)[6]

def MakeHeader(fname,n,k,size):
    return string.join(['RS_PARITY_PIECE_HEADER','FILE',fname,
                        'n',`n`,'k',`k`,'size',`size`,'piece'],
                       headerSep) + headerSep

def ParseHeader(header):
    return string.split(header,headerSep)

def ReadEncodeAndWriteBlock(readSize,inFD,outFD,code):
    buffer = array('B')
    buffer.fromfile(inFD,readSize)
    for i in range(readSize,code.k):
        buffer.append(0)
    codeVec = code.Encode(buffer)
    for j in range(code.n):
        outFD[j].write(struct.pack('B',codeVec[j]))

def EncodeFile(fname,prefix,n,k):
    """
    Function:     EncodeFile(fname,prefix,n,k)
    Description:  Encodes the file named by fname into n pieces named
                  prefix.p_0, prefix.p_1, ..., prefix.p_n-1.  At least
                  k of these pieces are needed for recovering fname.
                  Each piece is roughly the size of fname / k (there
                  is a very small overhead due to some header information).

                  Returns a list containing names of files for the pieces.

                  Note n and k must satisfy 0 < k < n < 257.
                  Use the DecodeFiles function for decoding.
    """
    fileList = []
    if (n > 256 or k >= n or k <= 0):
        raise Exception, 'Invalid (n,k), need 0 < k < n < 257.'
    inFD = open(fname,'rb')
    inSize = GetFileSize(fname)
    header = MakeHeader(fname,n,k,inSize)
    code = RSCode(n,k,8,shouldUseLUT=-(k!=1))
    outFD = range(n)
    for i in range(n):
        outFileName = prefix + '.p_' + `i`
        fileList.append(outFileName)
        outFD[i] = open(outFileName,'wb')
        outFD[i].write(header + `i` + '\n')

    if (k == 1): # just doing repetition coding
        str = inFD.read(1024)
        while (str):
            map( lambda x: x.write(str), outFD)
            str = inFD.read(256)
    else: # do the full blown RS encodding
        for i in range(0, (inSize/k)*k,k):
            ReadEncodeAndWriteBlock(k,inFD,outFD,code)

        if ((inSize % k) > 0):
            ReadEncodeAndWriteBlock(inSize % k,inFD,outFD,code)

    return fileList

def ExtractPieceNums(fnames,headers):
    l = range(len(fnames))
    pieceNums = range(len(fnames))
    for i in range(len(fnames)):
        l[i] = ParseHeader(headers[i])
    for i in range(len(fnames)):
        if (l[i][0] != 'RS_PARITY_PIECE_HEADER' or
            l[i][2] != l[0][2] or l[i][4] != l[0][4] or
            l[i][6] != l[0][6] or l[i][8] != l[0][8]):
            raise Exception, 'File ' + `fnames[i]` + ' has incorrect header.'
        pieceNums[i] = int(l[i][10])
    (n,k,size) = (int(l[0][4]),int(l[0][6]),long(l[0][8]))
    if (len(pieceNums) < k):
        raise Exception, ('Not enough parity for decoding; needed '
                          + `l[0][6]` + ' got ' + `len(fnames)` + '.')
    return (n,k,size,pieceNums)

def ReadDecodeAndWriteBlock(writeSize,inFDs,outFD,code):
    buffer = array('B')
    for j in range(code.k):
        buffer.fromfile(inFDs[j],1)
    result = code.Decode(buffer.tolist())
    for j in range(writeSize):
        outFD.write(struct.pack('B',result[j]))

def DecodeFiles(fnames,outName):
    """
    Function:     DecodeFiles(fnames,outName)
    Description:  Takes pieces of a file created using EncodeFiles and
                  recovers the original file placing it in outName.
                  The argument fnames must be a list of at least k
                  file names generated using EncodeFiles.
    """
    inFDs = range(len(fnames))
    headers = range(len(fnames))
    for i in range(len(fnames)):
        inFDs[i] = open(fnames[i],'rb')
        headers[i] = inFDs[i].readline()
    (n,k,inSize,pieceNums) = ExtractPieceNums(fnames,headers)
    outFD = open(outName,'wb')
    code = RSCode(n,k,8)
    decList = pieceNums[0:k]
    code.PrepareDecoder(decList)
    for i in range(0, (inSize/k)*k,k):
        ReadDecodeAndWriteBlock(k,inFDs,outFD,code)
    if ((inSize%k)>0):
        ReadDecodeAndWriteBlock(inSize%k,inFDs,outFD,code)

# The following code is used to make the doctest package
# check examples in docstrings.

def _test():
    import doctest, file_ecc
    return doctest.testmod(file_ecc)

if __name__ == "__main__":
    _test()
    print 'Tests passed'
