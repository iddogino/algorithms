"""
This file contained classes that make up the Prefix Trees used in Huffman Coding
"""

# Base class for a tree node (Composite). Defines the abstract functions all Node classes should implement
class Node:
  def __init__(self):
    pass

  def getWeight(self):
    raise NotImplementedError("Should have implemented this")

  def isLeaf(self):
    raise NotImplementedError("Should have implemented this")

# Leaf node in the prefix tree. Contains a char and it's weight.
class LeafNode:
  def __init__(self, char, weight):
    self.char = char
    self.weight = weight

  def getWeight(self):
    return self.weight

  def getChar(self):
    return self.char

  def isLeaf(self):
    return True;

# This is an inner node that has two sub nodes (both have values) - zero (right) and one (left)
class BinaryNode:
  def __init__(self, zero, one):
    self.zero = zero
    self.one = one

  def getWeight(self):
    return self.zero.getWeight() + self.one.getWeight() # Recursively get the weight of childs

  def isLeaf(self):
    return False;

  def getNext(self, num):
    if num == 0:
      return self.zero
    elif num == 1:
      return self.one
    else:
      raise ValueError("Value shoud be 1 or 0")

# Routine - pops the tree from an array of trees with the lightest weight
def popLightest(arr):
  if len(arr) < 1:
    raise ValueError("Can't run on empty array")
  l = arr[0]
  for t in arr:
    if t.getWeight() < l.getWeight():
      l = t
  arr.remove(l)
  return l

# This class holds a complete prefix tree
class PrefixTree:

  # Construct an optimal prefix tree for a collection of chars (messages) and their weights, using the huffman coding algorithm
  def __init__(self, charWeights):
    trees = []
    for char in charWeights.keys():
      trees.append(LeafNode(char, charWeights[char]))

    # This is the interesting part of the algorithm.
    # It basically pops the 2 lightest trees, combines them and put them back in - until there is only one tree left
    while len(trees) > 1:
      (l1, l2) = (popLightest(trees), popLightest(trees))
      trees.append(BinaryNode(l1,l2))
    self.tree = trees[0]

  #Get the actuall tree (for traversal purposes)
  def getTree(self):
    return self.tree

  # Get an encoding symbol table based on the tree.
  # This method recursively traverses the tree to get all possible binary codes and their chars
  def getEncodeTable(self, prefix = "", tree = None):
    if tree is None:
      tree = self.tree #For method overloading, recursion purposes

    if tree.isLeaf():
      r = {}
      r[tree.getChar()] = prefix
      return r
    else:
      r = {}
      r.update(self.getEncodeTable(prefix+'0', tree.getNext(0)))
      r.update(self.getEncodeTable(prefix+'1', tree.getNext(1)))
      return r
