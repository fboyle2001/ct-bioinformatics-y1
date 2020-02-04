class Matrix:
    def __init__(self, rows, columns, data = []):
        self.data = []
        
        if len(data) == 0:
            for x in range(rows):
                self.data.append([None for y in range(columns)])
        else:
            exp = -1
            for row in data:
                if exp == -1:
                    exp = len(row)
                else:
                    if len(row) != exp:
                        raise IndexError

                self.data.append(row)

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
        Update a single cell of the matrix such that A(0, 0)
        is the upper-rightmost element and A(n - 1, m - 1) is
        the lower-leftmost element
        """
        if col > self.col_length() - 1 or col < 0:
            raise IndexError

        if row > self.row_length() - 1 or row < 0:
            raise IndexError

        self.data[row][col] = value

    def get(self, row, col):
        if col > self.col_length() - 1 or col < 0:
            raise IndexError

        if row > self.row_length() - 1 or row < 0:
            raise IndexError

        return self.data[row][col]

    def row_length(self):
        return len(self.data)

    def col_length(self):
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

    def find_min_pos(self):
        min_row = 0
        min_value = None

        for i, row in enumerate(self.data):
            m = min(row)
            if min_value == None or m < min_value:
                min_value = m
                min_row = i

        c_index = self.data[min_row].index(min_value)
        return (min_row, c_index)

    def row_sum(self, row):
        if row > self.row_length() - 1 or row < 0:
            raise IndexError

        return sum(self.data[row])

    def col_sum(self, col):
        if col > self.col_length() - 1 or col < 0:
            raise IndexError

        s = 0

        for row in self.data:
            s += row[col]

        return s

    def delete_row(self, row):
        if row > self.row_length() - 1 or row < 0:
            raise IndexError

        del self.data[row]

    def delete_col(self, col):
        if col > self.col_length() - 1 or col < 0:
            raise IndexError

        reduced_data = []

        for row in self.data:
            new_row = []
            for i, d in enumerate(row):
                if i != col:
                    new_row.append(d)

            reduced_data.append(new_row)

        self.data = reduced_data

    def add_col(self, data=[]):
        if len(data) != self.row_length():
            raise IndexError
        
        for i, row in enumerate(self.data):
            row.append(data[i])
            
    def add_row(self, data=[]):
        self.data.append(data)
        
def NJ():
    relations = Matrix(8, 8 , [
            [  0,  32,  48,  51,  50,  48,  98, 148],
            [ 32,   0,  26,  34,  29,  33,  84, 136],
            [ 48,  26,   0,  42,  44,  44,  92, 152],
            [ 51,  34,  42,   0,  44,  38,  86, 142],
            [ 50,  29,  44,  44,   0,  24,  89, 142],
            [ 48,  33,  44,  38,  24,   0,  90, 142],
            [ 98,  84,  92,  86,  89,  90,   0, 148],
            [148, 136, 152, 142, 142, 142, 148,   0]
        ])

    q_scores = Matrix(relations.row_length(), relations.col_length())
    r = relations.row_length()

    biggest_q = 0

    for i in range(0, q_scores.col_length()):
        for j in range(i + 1, q_scores.row_length()):
            q = (r - 1) * relations.get(i, j) - relations.row_sum(i) - relations.col_sum(j)
            
            if q > biggest_q:
                biggest_q = q
                
            q_scores.update(i, j, q)
            q_scores.update(j, i, q)

    for i in range(0, q_scores.col_length()):
        q_scores.update(i, i, biggest_q + 1)

    min_x, min_y = q_scores.find_min_pos()

    print(min_x, min_y)
    print(relations)

    #could min_y = min_x? don't think so

    if min_y > min_x:
        relations.delete_row(min_y)
        relations.delete_col(min_y)
        relations.delete_row(min_x)
        relations.delete_col(min_x)
    else:
        relations.delete_row(min_x)
        relations.delete_col(min_x)
        relations.delete_row(min_y)
        relations.delete_col(min_y)

    #now compute the new d(ab,c)

    #now need to shrink the relations matrix
    #then recompute the q scores matrix
    #repeat until 2x2
    #no efficiency marks for this

    print(relations)
    print(relations.row_length(), relations.col_length())

    relations.add_row([0, 0, 0, 0, 0, 0, 0])
    relations.add_col([0, 0, 0, 0, 0, 0, 0])

    print(relations)
    print(relations.row_length(), relations.col_length())

    row = relations.row_length() - 1

    #last spot is going to be 0
    for i in range(row):
        pass

    return relations

r = NJ()
