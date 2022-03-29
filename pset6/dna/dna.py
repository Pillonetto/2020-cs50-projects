import sys
import csv

def count_most(desired_seq, file_seq):
    accepted_desired = {"AGATC", "AGAT", "AATG", "TATC"}

    if desired_seq not in accepted_desired:
        return 0

    length = len(desired_seq)
    counter_max = 0

    for i in range(len(file_seq)):
        seq_counter = 0

        while True:
            #the start of sequence should be changed, even without the for loop; thats why its multiplied by the counter
            start = i + length * seq_counter
            if file_seq[start:start+length] == desired_seq:
                seq_counter += 1
            else:
                break

        counter_max = max(counter_max, seq_counter)

    return counter_max


def check(dictionary_list, AGATC, AATG, TATC):
    loop = len(dictionary_list)

    for i in range(loop):
        if ((str(AGATC) == dictionary_list[i]['AGATC']) and (str(AATG) == dictionary_list[i]['AATG']) and (str(TATC) ==  dictionary_list[i]['TATC'])):
            return dictionary_list[i]['name']
            exit()

    return "No match"

if len(sys.argv) != 3:
    print("Usage: python dna.py CSVfile DNAsequence")
    exit()

with open(sys.argv[1], "r") as csv_file:
    dict_list = []
    csv_reader = csv.DictReader(csv_file)

    for line in csv_reader:
        dict_list.append(line)


    with open(sys.argv[2], "r") as dna_seq:
        sequence = dna_seq.read()


        agatc = count_most("AGATC", sequence)
        aatg = count_most("AATG", sequence)
        tatc = count_most("TATC", sequence)


        print(f"{check(dict_list, agatc, aatg, tatc)}")

        exit()




