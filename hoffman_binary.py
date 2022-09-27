"""
Implementation of Hoffman Binary Tree (Encoding) in the context of Word2Vec
Reference: https://stackoverflow.com/questions/11587044/how-can-i-create-a-tree-for-huffman-encoding-and-decoding,
https://en.wikipedia.org/wiki/Huffman_coding
"""

import numpy as np
import queue
from itertools import count

class TreeNode:
    def __init__(self, vector=None, left=None, right=None):
        # Vector of inner units
        self.vector = vector

        # left node
        self.left = left

        # right node
        self.right = right
    
    def children(self):
        return((self.left, self.right))

# Creates a Hoffman binary tree based on word frequencies
def create_tree(word_counts, n):
    p = queue.PriorityQueue()

    # Create an index to deal with equal frequency comparisons
    index = count(0)                    
    for w, c in word_counts.items():    # 1. Create a leaf node for each symbol
        p.put((c, next(index), w))      # and add it to the priority queue

    while p.qsize() > 1:                # 2. While there is more than one node
        l, r = p.get(), p.get()         # 2a. remove two highest nodes
        init_vector = np.random.uniform(-1, 1, (n, 1))
        node = TreeNode(vector=init_vector, left=l, right=r)        # 2b. create internal node with children
        p.put((l[0]+r[0], next(index), node))                       # 2c. add new node to queue      

    return p.get()                      # 3. tree is complete - return root node

# Creates Hoffman coding based on the tree paths
def create_code(root):
    code_dict = {}
    traverse_helper(root, [], code_dict)

    return code_dict

# Recursive helper function to traverse the Hoffman tree
def traverse_helper(node, code, ret_dict):
    if type(node[2]) == str:
        print(node, code)
        temp = code.copy()  # Prevents code from changing in-place
        ret_dict[node[2]] = temp
        code.pop()
        
        return
    
    traverse_helper(node[2].left, code + [0], ret_dict)
    traverse_helper(node[2].right, code + [1], ret_dict)

# Returns a tuple of tree nodes and path direction based on an input word
def get_path_nodes(word, code_dict, root):
    code = code_dict[word]
    nodes = []
    cur = root[2]

    for direction in code:
        nodes.append((cur, direction))
        
        if direction == 0:
            cur = cur.left[2]
        
        else:
            cur = cur.right[2]

    return nodes


if __name__ == '__main__':
    word_counts = {'natural': 1, 'language': 1, 'processing': 1, 'and': 2, 'machine': 1, 'learning': 1, 'is': 1, 'fun': 1, 'exciting': 1}

    freq = [
    (8.167, 'a'), (1.492, 'b'), (2.782, 'c'), (4.253, 'd'),
    (12.702, 'e'),(2.228, 'f'), (2.015, 'g'), (6.094, 'h'),
    (6.966, 'i'), (0.153, 'j'), (0.747, 'k'), (4.025, 'l'),
    (2.406, 'm'), (6.749, 'n'), (7.507, 'o'), (1.929, 'p'), 
    (0.095, 'q'), (5.987, 'r'), (6.327, 's'), (9.056, 't'), 
    (2.758, 'u'), (1.037, 'v'), (2.365, 'w'), (0.150, 'x'),
    (1.974, 'y'), (0.074, 'z') ]

    freq = dict(freq)
    freq = dict((v,k) for k,v in freq.items())

    root = create_tree(word_counts, 10)
    code_dict = create_code(root)
    #nodes = get_path_nodes('processing', code_dict, root)
    

