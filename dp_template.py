#!/usr/bin/python
import time
import sys


# YOUR FUNCTIONS GO HERE -------------------------------------

def find_alignment(seq1, seq2):
    backtrack_matrix = [[None for x in range(len(seq1) + 1)] for y in range(len(seq2) + 1)]
    scoring_matrix = [[None for x in range(len(seq1) + 1)] for y in range(len(seq2) + 1)]
    directions = {"L": (-1, 0), "U": (0, -1), "D": (-1, -1)}

    #fill in top row and top column then repeat for top-1 row and top-1 column
    #... until reach 1x1 bottom right corner

    
    print(backtrack_matrix)
    pass

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

