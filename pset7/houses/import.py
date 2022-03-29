import cs50
import sys
from csv import DictReader

if len(sys.argv) != 2:
    print("Usage: import.py file.csv")
    exit()


with open(sys.argv[1], "r") as in_file:

    reader = DictReader(in_file)

    output = cs50.SQL("sqlite:///students.db")

    for row in reader:

        tmp_name = row['name']
        name_list = tmp_name.split(" ")

        tmp_house = row['house']
        tmp_birth = row['birth']

        if len(name_list) == 2:
            output.execute('INSERT INTO students (first, last, house, birth) VALUES (?, ?, ?, ?)',
                            name_list[0], name_list[1], tmp_house, tmp_birth)

        elif len(name_list) == 3:
            output.execute('INSERT INTO students (first, middle, last, house, birth) VALUES (?, ?, ?, ?, ?)',
                            name_list[0], name_list[1], name_list[2], tmp_house, tmp_birth)
