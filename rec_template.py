#!/usr/bin/python
import time
import sys


# YOUR FUNCTIONS GO HERE -------------------------------------

def find_alignment(seq1, seq2, cseq1, cseq2, cscr, count):
    if len(seq1) == 0 and len(seq2) == 0:
        #used all characters
        return (cscr, [cseq1, cseq2], 1)

    if len(seq1) == 0 and len(seq2) != 0:
        c2 = seq2[len(seq2) - 1]
        return find_alignment(seq1, seq2[:len(seq2) - 1], "-" + cseq1, c2 + cseq2, score("-", c2) + cscr, count + 1)

    if len(seq1) != 0 and len(seq2) == 0:
        c1 = seq1[len(seq1) - 1]
        return find_alignment(seq1[:len(seq1) - 1], seq2, c1 + cseq1, "-" + cseq2, score(c1, "-") + cscr, count + 1)
        
    c1 = seq1[len(seq1) - 1]
    c2 = seq2[len(seq2) - 1]

    #case 1: try both characters
    case1 = find_alignment(seq1[:len(seq1) - 1], seq2[:len(seq2) - 1], c1 + cseq1, c2 + cseq2, score(c1, c2) + cscr, count)

    #case 2: try seq1_char with a gap
    case2 = find_alignment(seq1[:len(seq1) - 1], seq2, c1 + cseq1, "-" + cseq2, score(c1, "-") + cscr, count)

    #case 3: try seq2_char with a gap
    case3 = find_alignment(seq1, seq2[:len(seq2) - 1], "-" + cseq1, c2 + cseq2, score("-", c2) + cscr, count)
    
    scores = [case1[0], case2[0], case3[0]]
    aligns = [case1[1], case2[1], case3[1]]
    count += case1[2] + case2[2] + case3[2]
    #print(scores, aligns)
    best_score = max(scores)
    best_index = scores.index(best_score)
    best_align = aligns[best_index]

    return (best_score, best_align, count)

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
# Call any functions you need here, you can define them above.
# To work with the printing functions below the best alignment should be called best_alignment and its score should be called best_score. 
# The number of alignments you have checked should be stored in a variable called num_alignments.

best_score, best_alignment, num_alignments = find_alignment(seq1, seq2, "", "", 0, 0)

#-------------------------------------------------------------


# DO NOT EDIT ------------------------------------------------
# This calculates the time taken and will print out useful information 
stop = time.time()
time_taken=stop-start

# Print out the best
print('Alignments generated: '+str(num_alignments))
print('Time taken: '+str(time_taken))
print('Best (score '+str(best_score)+'):')
displayAlignment(best_alignment)

#-------------------------------------------------------------
