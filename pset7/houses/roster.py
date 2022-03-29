# TODO
import sys
import cs50

if len(sys.argv) != 2:
    print("Usage: python roster.py <house>")
    exit()

db = cs50.SQL('sqlite:///students.db')

des_house = sys.argv[1]

student_names = db.execute('SELECT first, middle, last FROM students WHERE house = (?) ORDER BY last', des_house)

student_birth = db.execute('SELECT birth FROM students WHERE house = (?) ORDER BY last', des_house)

for x in range(len(student_birth)):

    if student_names[x]['middle'] != None:
        print(f"{student_names[x]['first']} {student_names[x]['middle']} {student_names[x]['last']}, born {student_birth[x]['birth']}")

    else:
        print(f"{student_names[x]['first']} {student_names[x]['last']}, born {student_birth[x]['birth']}")