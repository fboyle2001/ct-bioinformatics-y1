import random
import sys

def generate_matrix(size, name):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    species = [x for x in alphabet[:size]]

    data = []

    for i, s in enumerate(species):
        col = []
        for j, q in enumerate(species):
            if i > j:
                col.append(data[j][i])
                continue
            if i == j:
                col.append(0)
                continue

            col.append(random.randint(14, 200))
        data.append(col)

    file = open(name, "w+")

    write_data = ""

    for s in ["-"] + species:
        if write_data != "":
            write_data += " "
        write_data += s

    write_data += "\n"

    for i, s in enumerate(species):
        write_data += s + " "
        for d in data:
            write_data += str(d[i]) + " "
        write_data += "\n"

    file.write(write_data)
    file.close()

size = int(sys.argv[1])
name = sys.argv[2]
generate_matrix(size, name)
