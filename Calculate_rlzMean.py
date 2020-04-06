import shutil
import sys
from itertools import count
import os
import re
import functools

def parse_curve(filename):
    input_file = open(filename, "r")
    data = []
    line_count = 0
    lines = input_file.readlines()
    for line in lines:
        line_count += 1
        string_values = line.split(",")
        if line_count <= 2:
            data.append(string_values)
        else:
            float_values = []
            for string_value in string_values:
                float_values.append(float(string_value))
            data.append(float_values)
    input_file.close()
    return data

def parse_realization(filename):
    input_file = open(filename, "r")
    names = []
    line_count = 0
    lines = input_file.readlines()
    for line in lines:
        line_count += 1
        if line_count > 1 and line_count % 2 == 0:
            names.append(line.split(",")[1])
    input_file.close()
    return names

def file_op(output_filename, data1, data2, data_filename1, data_filename2):
    output_file = open(output_filename, "w")
    try:
        print("Calculating realization "+output_filename+" with "+data_filename1+" and "+data_filename2+"...")

        #print(data1)
        #print(data2)
        row_count1 = len(data1)
        row_count2 = len(data2)

        row_count = max(row_count1, row_count2)
        for row in range (0, row_count):

            if row < 2:
                output_file.write(",".join(data1[row]))
            else:
                row1 = []
                row2 = []
                if row < row_count1:
                    row1 = data1[row]
                if row < row_count2:
                    row2 = data2[row]

                col_count1 = len(row1)
                col_count2 = len(row2)
                col_count = max(col_count1, col_count2)
                for col in range(0, col_count):
                    data_point1 = row1[col]
                    data_point2 = row2[col]

                    if col > 0:
                        output_file.write(",")
                    if col > 2:
                        output_file.write(str((data_point1 + data_point2) * 0.5))
                    else:
                        output_file.write(str(data_point1))
                output_file.write("\n")
    finally:
        output_file.close()
    return 0

def format_directory(directory):
    if not directory.endswith("/"):
        directory += "/"
    return directory

def custom_filename_compare(f1, f2):
    n1 = re.findall(r'\d+', f1)
    n2 = re.findall(r'\d+', f2)
    return int(n1[0]) - int(n2[0])

def main():
    args = len(sys.argv)

    if args <= 3:
        print("Use as Calculate_rlzMean.py realizations.csv ./input-folder/ ./output-folder/")
        exit(0)

    # folders
    realization_name = sys.argv[1]
    input_directory = format_directory(sys.argv[2])
    output_directory = format_directory(sys.argv[3])

    # clear output
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.mkdir(output_directory)

    index = 0
    realization_names = parse_realization(realization_name)
    data_file1 = 0
    data_file2 = 0
    previous_filename = 0
    for filename in sorted(os.listdir(input_directory), key=functools.cmp_to_key(custom_filename_compare)):
        data = parse_curve(input_directory+""+filename)
        if index % 2 == 0:
            data_file1 = data
            previous_filename = filename
        else:
            realization_index = int(index / 2)
            data_file2 = data
            file_op(output_directory+realization_names[realization_index]+".csv", data_file1, data_file2, previous_filename, filename)

        index += 1
    #print(realization_names)

    print("Done!")

if __name__ == '__main__':
    main()




