#!/usr/bin/python

"""
This script encodes text files using Huffman Coding, in order to compress their volume. 
The script analyzes the text to generate the 'weight' of each char, builds the prefix tree using the Huffman Coding algorithm, and saves the result into a binary file.
The script has to be run with one parameter - name of file to encode. It'll save (overwrite if exists) a file named ORIGINAL_FILE_NAME.hc.
The result file has both the char weights and the data. It is format as following:

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
from bitstring import BitArray # Used to create the binary file. See - http://pythonhosted.org/bitstring/index.html

"""General routines"""
#Manages a progress counter (for part/sum)
def update_progress(part, sum):
  progress = int((float(part)/float(sum))*100.0)
  sys.stdout.write('\r[{0}] {1}%'.format('#'*(progress/10), progress))
  sys.stdout.flush()

#Read & count chars in file to calculate weight
def countChars(sourceFile):
  char_weights = {}
  line = 0
  for s_line in sourceFile:
    line += 1
    update_progress(line, lineCount)
    for s_char in s_line:
      #Insert to dict
      if s_char in char_weights:
        char_weights[s_char] += 1
      else:
        char_weights[s_char] = 1
  return char_weights

"""Input validation"""
# Validate file name is supplied
if len(sys.argv) < 2:
  raise Exception("No file supplied");

"""Script"""
#Open source file and get line count
sourceFile = open(sys.argv[1], 'r')
lineCount = sum(1 for line in sourceFile)
sourceFile = open(sys.argv[1], 'r')

#Analyze file (build dictionary of file weights)
print 'Analyzing file'
charWeights = countChars(sourceFile)
print '\n'

#Create symbol table based on file analasys
symbolTable = PrefixTree(charWeights).getEncodeTable()

#Initialize output bits with count of chars
outputBits = BitArray(int=len(charWeights), length=8)

#Add char weights to binary output
for char in charWeights.keys():
  outputBits.append(BitArray(int=ord(char), length=32))
  outputBits.append(BitArray(int=charWeights[char], length=32))

#Add code words
print 'Encoding file'
line = 0
sourceFile = open(sys.argv[1], 'r')
for s_line in sourceFile:
  line += 1
  update_progress(line, lineCount)
  for s_char in s_line:
    outputBits.append(BitArray('0b{}'.format(symbolTable[s_char])))
print '\n'

#Write compressed binary to file
outFile = open('{}.hc'.format(sys.argv[1]), 'wb')
outputBits.tofile(outFile)
print 'Done.'
