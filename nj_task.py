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
        max_char_size = 0

        for row in self.data:
            mi = len(str(min(row)))
            ma = len(str(max(row)))

            if mi > max_char_size:
                max_char_size = mi

            if ma > max_char_size:
                max_char_size = ma

        display_rows = []
        

        for row in self.data:
            disp_row = []
            for char in row:
                c = str(char)

                c = (max_char_size - len(c) + 1) * " " + c
                disp_row.append(c)
            display_rows.append(disp_row)

        out = ""

        for row in display_rows:
            if out != "":
                out += "\n"

            out += "["
                
            for c in row:
                #if out[-1] != "[":
                #    out += ","
                out += c

            out += "]"

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
        """
        Finds min position excluding the diagonal elements
        """
        min_row = 0
        min_value = None

        for i, row in enumerate(self.data):
            m = min(row[:i] + row[i+1:])
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

    def replace_row(self, row, data):
        self.data[row] = data

    def replace_col(self, col, data):
        for i in range(0, self.col_length()):
            self.data[i][col] = data[i]
        
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

    while q_scores.row_length() != 2:
        r = relations.row_length()

        for i in range(0, q_scores.col_length()):
            q_scores.update(i, i, 0)
            for j in range(i + 1, q_scores.row_length()):
                q = (r - 1) * relations.get(i, j) - relations.row_sum(i) - relations.col_sum(j)
                    
                q_scores.update(i, j, q)
                q_scores.update(j, i, q)
        
        print("n =", relations.col_length())
        print("Relation Matrix:")
        print(relations)
        print()
        print("Q-Score Matrix:")
        print(q_scores)
        print()

        #have relation scores and q_scores

        min_x, min_y = q_scores.find_min_pos()

        #going to remove these 2 so need to work out the scores first

        new_scores = []

        #calculate the d(ab, c) scores

        for i in range(0, q_scores.col_length()):
            if i == min_x or i == min_y:
                continue
            
            dab_c = relations.get(min_x, i) + relations.get(min_y, i) - relations.get(min_x, min_y)
            dab_c /= 2
            new_scores.append(dab_c)

        #print("Matrix is", relations.row_length(), relations.col_length())

        #delete the species with a higher index in the matrix
        #avoids having to correc min_y or min_x since they cannot equal each other

        if min_y > min_x:
            relations.delete_row(min_y)
            relations.delete_col(min_y)
            
            q_scores.delete_row(min_y)
            q_scores.delete_col(min_y)
            
            new_scores.insert(min_x, 0)
            
            relations.replace_row(min_x, new_scores)
            relations.replace_col(min_x, new_scores)
        else:
            relations.delete_row(min_x)
            relations.delete_col(min_x)
            
            q_scores.delete_row(min_x)
            q_scores.delete_col(min_x)
            
            new_scores.insert(min_y, 0)
            
            relations.replace_row(min_y, new_scores)
            relations.replace_col(min_y, new_scores)
            
        #print("Matrix is", relations.row_length(), relations.col_length())
        #print(relations)

    return relations

r = NJ()
