#!/usr/bin/python
import time
import sys


# YOUR FUNCTIONS GO HERE -------------------------------------

class Matrix:
    def __init__(self, rows, columns):
        self.data = []
        
        for x in range(rows):
            self.data.append(["" for y in range(columns)])

    def __str__(self):
        out = ""
        
        for row in self.data:
            if out != "":
                out += "\n"
                
            out += str(row)

        return out

    def __repr__(self):
        return str(self)

    def update(self, row, col, value):
        """
        Update a single cell of the matrix uses conventional numbering
        such that A(1, 1) is the upper-rightmost element and A(n, m) is
        the lower-leftmost element
        """
        if col > len(self.data[0]) or col < 1:
            raise IndexError

        if row > len(self.data) or row < 1:
            raise IndexError

        self.data[row - 1][col - 1] = value

def find_local_alignment(seq1, seq2):
    scoring_mtx = Matrix(len(seq1) + 1, len(seq2) + 1)
    backtrack_mtx = Matrix(len(seq1) + 1, len(seq2) + 1)
    print(scoring_mtx)
    print()
    print(backtrack_mtx)

    for x in range(len(seq1) + 1):
        #fill row then fill col then fill 1 diagonal
        for y in range(x, len(seq1) + 1):l
            #do s(x,y) and s(y,x)

def s(x, y, scoring_matrix):
    pass
            
def score(c1, c2):
    if c1 == c2:
        if c1 == "A":
            return 3
        elif c1 == "C":
            return 2
        elif c1 == "G":
            return 1
        elif c1 == "T":
            return 2
        #matching gaps shouldn't happen
    else:
        if c1 == "-" or c2 == "-":
            return -4
        else:
            return -3        

# ------------------------------------------------------------



# DO NOT EDIT ------------------------------------------------
# Given an alignment, which is two strings, display it

def displayAlignment(alignment):
    string1 = alignment[0]
    string2 = alignment[1]
    string3 = ''
    for i in range(min(len(string1),len(string2))):
        if string1[i]==string2[i]:
            string3=string3+"|"
        else:
            string3=string3+" "
    print('Alignment ')
    print('String1: '+string1)
    print('         '+string3)
    print('String2: '+string2+'\n\n')

# ------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This opens the files, loads the sequences and starts the timer
file1 = open(sys.argv[1], 'r')
seq1=file1.read()
file1.close()
file2 = open(sys.argv[2], 'r')
seq2=file2.read()
file2.close()
start = time.time()

#-------------------------------------------------------------


# YOUR CODE GOES HERE ----------------------------------------
# The sequences are contained in the variables seq1 and seq2 from the code above.
# To work with the printing functions below the best local alignment should be called best_alignment and its score should be called best_score. 



#-------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This calculates the time taken and will print out useful information 
stop = time.time()
time_taken=stop-start

# Print out the best
print('Time taken: '+str(time_taken))
print('Best (score '+str(best_score)+'):')
displayAlignment(best_alignment)

#-------------------------------------------------------------

