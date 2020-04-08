import shutil
import sys
from itertools import count
import os

def main():
    args = len(sys.argv)

    if args < 2:
        print("Use as SegmentInput.py input.csv ./output-folder/")
        exit(0)

    print("Opening "+sys.argv[1]+" and writing to "+sys.argv[2])
    input_file = open(sys.argv[1], "r")
    output_file = open(sys.argv[2], "w")

    output_file.write("ID, X, Y\n")
    line_count = 0
    lines = input_file.readlines()
    for line in lines:
        line_count += 1
        if line_count == 1:
            continue

        variables = line.split(",")
        variable_count = len(variables)
        coord_id = variables[5]

        variable_counter = 0
        for i in range (11, variable_count-3):
            if variables[i] == "":
                break
            if variable_counter % 2 == 0:
                output_file.write(coord_id + "," + variables[i] + ",")
            else:
                output_file.write(variables[i] + "\n")
            variable_counter = variable_counter + 1

    input_file.close()
    output_file.close()

    print("Done!")

if __name__ == '__main__':
    main()



