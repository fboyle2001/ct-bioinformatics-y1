class Matrix:
    def __init__(self, data, association):
        self.data = data
        self.association = [str(x) for x in association]

    def __str__(self):
        #find the longest thing
        max_char_size = 0

        for row in self.data:
            mi = len(str(min(row)))
            ma = len(str(max(row)))

            if mi > max_char_size:
                max_char_size = mi

            if ma > max_char_size:
                max_char_size = ma
                
        tag_len = max([len(x) for x in self.association] + [len("Sum")])
        display_rows = []
        max_char_size = max(tag_len, max_char_size)

        top_row = (tag_len + 4) * " "

        for tag in self.association:
            t = (max_char_size - len(tag) + 1) * " " + tag
            top_row += t

        row_sums = []
        
        for row in self.data:
            disp_row = []
            
            for char in row:
                c = str(char)
                c = (max_char_size - len(c) + 1) * " " + c
                disp_row.append(c)
                
            r_sum = sum(row)
            row_sums.append((max_char_size - len(c) + 1) * " " + str(r_sum))
            display_rows.append(disp_row)

        max_row_sum_len = max([len(str(x)) for x in row_sums])
        top_row += (max_row_sum_len - 1) * " " + "Sum"
        display_rows.insert(0, top_row)

        out = ""

        for i, row in enumerate(display_rows):
            if out != "":
                out += "\n"

            if i == 0:
                out += row
            else:
                tag = self.association[i - 1]
                tag += (tag_len - len(tag)) * " " 
                out += tag + " | ["
                    
                for c in row:
                    out += c

                out += "] "
                out += row_sums[i - 1]

        return out
    
    def __repr__(self):
        return str(self)

    def update(self, row, col, value):
        self.data[row][col] = value

    def get(self, row, col):
        return self.data[row][col]

    def row_length(self):
        return len(self.data)

    def col_length(self):
        return len(self.data[0])

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
        return sum(self.data[row])

    def col_sum(self, col):
        s = 0

        for row in self.data:
            s += row[col]

        return s

    def delete_row(self, row):
        del self.data[row]

    def delete_col(self, col):
        reduced_data = []

        for row in self.data:
            new_row = []
            for i, d in enumerate(row):
                if i != col:
                    new_row.append(d)

            reduced_data.append(new_row)

        self.data = reduced_data

    def replace_row(self, row, data):
        self.data[row] = data

    def replace_col(self, col, data):
        for i in range(0, self.col_length()):
            self.data[i][col] = data[i]

    def merge_associated(self, x, y):
        if x > y:
            tag_y = self.association[y]
            self.association[x] = tag_y + self.association[x]
            del self.association[y]
        else:
            tag_x = self.association[x]
            self.association[y] = tag_x + self.association[y]
            del self.association[x]
        
def NJ(file_name):
    file = open(file_name, "r")
    lines = file.read().split("\n")
    file.close()

    species = lines[0].split(" ")[1:]
    relation_data = []
    q_scores_data = []

    for i in range(1, len(lines)):
        row = lines[i].strip().split(" ")[1:]

        num_row = [int(x) for x in row]
        q_row = [None for x in num_row]
        
        relation_data.append(num_row)
        q_scores_data.append(q_row)

    relations = Matrix(relation_data, [x for x in species])
    q_scores = Matrix(q_scores_data, [x for x in species])

    while q_scores.row_length() != 1:
        r = relations.row_length()

        for i in range(0, q_scores.col_length()):
            q_scores.update(i, i, 0)
            for j in range(i + 1, q_scores.row_length()):
                q = (r - 1) * relations.get(i, j) - relations.row_sum(i) - relations.col_sum(j)
                    
                q_scores.update(i, j, q)
                q_scores.update(j, i, q)
                
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

        #delete the species with a higher index in the matrix
        #avoids having to correct min_y or min_x since they cannot equal each other
        
        relations.merge_associated(min_x, min_y)
        q_scores.merge_associated(min_x, min_y)

        if min_y > min_x:
            #might be worth just swapping min_y and min_x?
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
