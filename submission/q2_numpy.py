#!/usr/bin/python
import time
import sys
import numpy as np

# YOUR FUNCTIONS GO HERE -------------------------------------

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

def get_max_position(array):
    max_pos = None
    max_value = None

    for x, row in enumerate(array):
        for y, value in enumerate(row):
            if max_value == None or value > max_value:
                max_value = value
                max_pos = (x, y)

    return max_pos

#5000 * 5000 in 131s
def find_local_alignment(seq1, seq2):
    scoring = np.zeros(shape=(len(seq1) + 1, len(seq2) + 1), dtype=int)
    backtrack = np.zeros(shape=(len(seq1) + 1, len(seq2) + 1), dtype=str)

    #fill in first col and row with ends and scores of 0
    #the scores are prefilled with 0s via numpy

    backtrack[0][0] = "E"

    for i in range(1, len(seq1) + 1):
        backtrack[i][0] = "E"

    for j in range(1, len(seq2) + 1):
        backtrack[0][j] = "E"

    #now fill in each submatrix constantly getting smaller

    #not sure about this check
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            up = scoring[i - 1][j] - 4 #must match with gap
            left = scoring[i][j - 1] - 4 #must match with gap
            diagonal = scoring[i - 1][j - 1] + score(seq1[i - 1], seq2[j - 1])

            value = max(0, up, left, diagonal)

            if value == 0:
                backtrack[i][j] = "E"
            elif diagonal >= up and diagonal >= left:
                backtrack[i][j] = "D"
            elif up >= diagonal and up >= left:
                backtrack[i][j] = "U"
            elif left >= diagonal and left >= up:
                backtrack[i][j] = "L"

            scoring[i][j] = value
    
    #find the maximum matrix entries coordinates
    x, y = get_max_position(scoring)

    #start from the maximum and work backwards
    last_direction = backtrack[x][y]
    cseq1 = ""
    cseq2 = ""

    alignment_score = scoring[x][y]

    #move continually until we hit an end
    #directions represent a change in x, y coords 
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

        last_direction = backtrack[x][y]

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

#a = find_local_alignment("GAATTCAATA", "GAATTCTAAC")
#print(a)

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

