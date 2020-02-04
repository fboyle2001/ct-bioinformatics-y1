import itertools
import time
import sys

scores = [
    
        [-9,  -8,-12,-16,-20,-24,-23,-27,-31],
        [-3,   3,  4,  0, -4, -8,-12,-16,-20],
        [-7,  -1,  0,  6,  2, -2, -6,-10,-14],
        [-11, -5, -4, -1, -5, -9,-13,-10,-16],
        [-13,-12, -6,  0,  7,  8,  4,-17,  1],
        [-13, -7,-11,-12, -5,  2,  8,  0,  0],
        [-17,-11, -5,  1,  8, 15, 11,  4, 13],
        [-21,-15, -9, -3,  4, 11, 12,  8, 14],
        [-29,-23,-17,-11, -9, -2,  4,  5,  6]
        
]

class TestResult:
    def __init__(self, delta, score, align, count):
        self.delta = delta
        self.score = score
        self.align = align
        self.count = count

def generate_input_combinations():
    input_files_a = []
    input_files_b = []

    for i in range(3, 12):
        input_files_a.append("length" + str(i) + "_A.txt")
        input_files_b.append("length" + str(i) + "_B.txt")

    return list(itertools.product(input_files_a, input_files_b))

def run_single_test(inputA, inputB):
    file1 = open(inputA, 'r')
    seq1=file1.read()
    file1.close()
    
    file2 = open(inputB, 'r')
    seq2=file2.read()
    file2.close()
    
    start = time.time()
    
    best_score, best_alignment, num_alignments = find_alignment(seq1, seq2, "", "", 0, 0)

    end = time.time()

    return TestResult(end - start, best_score, best_alignment, num_alignments)

def run_tests():
    combinations = generate_input_combinations()
    total_time = 0
    fails = 0
    passes = 0

    for combination in combinations:
        result = run_single_test(*combination)
        inputA_no = int(combination[0].split("_")[0].split("length")[1]) - 3
        inputB_no = int(combination[1].split("_")[0].split("length")[1]) - 3
        print("Testing", combination)
        expected_score = scores[inputB_no][inputA_no]

        if expected_score != result.score:
            print("FAILED:", combination, "expected:", expected_score, "got:", result.score)
            print(result.score)
            print(result.align)
            print(result.count)
            fails += 1
        else:
            print("PASS:", combination)
            passes += 1
            
        print("Ran", combination, "in", str(result.delta) + "s")
        total_time += result.delta

    print(passes, "/", (passes + fails), "tests passed")
    print("Took", total_time + "s", "in total")
            
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

run_tests()
