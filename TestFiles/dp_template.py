#!/usr/bin/python
import time
import sys

# YOUR FUNCTIONS GO HERE -------------------------------------

class Matrix:
    def __init__(self, rows, columns):
        self.data = []
        
        for x in range(rows):
            self.data.append([None for y in range(columns)])

    def __str__(self):
        out = ""
        
        for row in self.data:
            if out != "":
                out += "\n"
                
            out += str([x if x != None else " " for x in row ])

        return out

    def __repr__(self):
        return str(self)

    def update(self, row, col, value):
        """
        Update a single cell of the matrix uses conventional numbering
        such that A(1, 1) is the upper-rightmost element and A(n, m) is
        the lower-leftmost element
        """
        if col > self.row_length() - 1 or col < 0:
            raise IndexError

        if row > self.col_length() - 1 or row < 0:
            raise IndexError

        self.data[row][col] = value

    def get(self, row, col):
        if col > self.row_length() - 1 or col < 0:
            raise IndexError

        if row > self.col_length() - 1 or row < 0:
            raise IndexError

        return self.data[row][col]

    def col_length(self):
        return len(self.data)

    def row_length(self):
        return len(self.data[0])

    def find_max_pos(self):
        max_row = 0
        max_value = 0

        for i, row in enumerate(self.data):
            m = max(row)
            if m > max_value:
                max_value = m
                max_row = i

        c_index = self.data[max_row].index(max_value)
        return (max_row, c_index)

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
        
def find_local_alignment(seq1, seq2):
    scoring = Matrix(len(seq1) + 1, len(seq2) + 1)
    backtrack = Matrix(len(seq1) + 1, len(seq2) + 1)

    #fill in the first row and column using s(0, i) and s(i, 0) = -2i
    #do it seperately because row_length != col_length

    scoring.update(0, 0, 0)
    backtrack.update(0, 0, "E")

    for i in range(1, scoring.col_length()):
        scoring.update(i, 0, 0)
        backtrack.update(i, 0, "E")

    for j in range(1, scoring.row_length()):
        scoring.update(0, j, 0)
        backtrack.update(0, j, "E")

    #now fill in each submatrix constantly getting smaller

    for i in range(1, scoring.col_length()):
        for j in range(1, scoring.row_length()):
            up = scoring.get(i - 1, j) - 4 #must match with gap
            left = scoring.get(i, j - 1) - 4 #must match with gap
            diagonal = scoring.get(i - 1, j - 1) + score(seq1[i - 1], seq2[j - 1])

            value = max(0, up, left, diagonal)

            if value == 0:
                backtrack.update(i, j, "E")
            elif diagonal >= up and diagonal >= left:
                backtrack.update(i, j, "D")
            elif up >= diagonal and up >= left:
                backtrack.update(i, j, "U")
            elif left >= diagonal and left >= up:
                backtrack.update(i, j, "L")

            scoring.update(i, j, value)

    x, y = scoring.find_max_pos()

    movement = {"U": (0, -1), "L": (-1, 0), "D": (-1, -1)}
    
    last_direction = backtrack.get(x, y)
    cseq1 = ""
    cseq2 = ""

    alignment_score = scoring.get(x, y)
    
    while last_direction != "E":
        if last_direction == "L":
            y += -1
            cseq1 = "-" + cseq1
            cseq2 = seq2[y] + cseq2
        elif last_direction == "D":
            x += -1
            y += -1
            cseq1 = seq1[x] + cseq1
            cseq2 = seq2[y] + cseq2
        elif last_direction == "U":
            x += -1
            cseq1 = seq1[x] + cseq1
            cseq2 = "-" + cseq2

        last_direction = backtrack.get(x, y)

    return ((cseq1, cseq2), alignment_score)

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


best_alignment, best_score = find_local_alignment(seq1, seq2)


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

