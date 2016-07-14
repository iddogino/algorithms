#!/usr/bin/python

"""
This script decodes a Huffman Coded text file supplied to it. 
It takes the name of the encoded file as it's only input, and saves a file named the same (with .txt added to it) after running.

Input binary file format as follows:

HEADER:
  Charechter count (amount of unique symbols in text) [8 bits]
  For each unique charechter: [Total - count * 64 bits]
    The charechter code [32 bits]
    The charechter weight [32 bits]
DATA:
  Encoded text (padded with between 0 to 7 zeros at the end to round up to bytes)
"""

"""Imports"""
import sys # For command args
from PrefixTree import PrefixTree # Class to construct and work with the PrefixTree
from bitstring import ConstBitStream # Used to read the binary file as a stream. See - http://pythonhosted.org/bitstring/index.html


"""General routines"""
#Manages a progress counter (for part/sum)
def update_progress(part):
  progress = part%200000
  sys.stdout.write('\r              ')
  sys.stdout.write('\rDecoding{0}'.format('.'*(progress/50000)))
  sys.stdout.flush()

"""Input validation"""
# Validate file name is supplied
if len(sys.argv) < 2:
  raise Exception("No file supplied");

"""Script"""
#Open source file and construct the bit stream
sourceFile = open(sys.argv[1], 'rb')
sourceBits = ConstBitStream(bytes=sourceFile.read())

#Read the char weights from the bit stream
countOfChars = sourceBits.read('int:8')
charWeights = {}

for i in range(0,countOfChars):
	c = chr(sourceBits.read('int:32'))
	w = sourceBits.read('int:32')
	charWeights[c] = w

#Construct PrefixTree based on char weights
pTree = PrefixTree(charWeights).getTree()

#Read & decode chars. Saves to final file:
outFile = open('{}.txt'.format(sys.argv[1]), 'w')
while len(sourceBits) - sourceBits.pos > 0:
	update_progress(sourceBits.pos)
	p = pTree
	while not p.isLeaf():
		bit = 1 if sourceBits.read('bin:1') == '1' else 0
		p = p.getNext(bit)
	
	outFile.write(p.getChar())

#Close file
outFile.close()
print 'Done.'
