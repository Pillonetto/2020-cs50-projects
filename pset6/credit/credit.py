from cs50 import get_int

def sum_digits(number):
    sum_digit = 0
    for i in range(len(number)):
        sum_digit += int(number[i])

    return sum_digit

def double(number):
    if number == 0:
        return 0
    else:
        return number * 2


number = get_int("Number: ")
string_num = str(number)
final_sum = 0
extra = [0]
contagem = 0


for i in range(0, len(string_num), 2):
    to_add = int(string_num[i]) * 2
    extra.append(f"{str(to_add)}")


for i in range(len(extra)):
    if extra[i - 1][1] != NULL:
        final_sum += sum_digits(extra[i])

    else:
        final_sum += extra[i]


for i in range(1, 2, len(string_num)):
    final_sum += int(string_num[i])


if final_sum % 10 == 0:
    if extra[0] == 3 and extra[1] in [4,7]:
        print("AMEX")
    elif extra[0] == 5 and extra[1] in range(5):
        print("MasterCard")
    elif extra[0] == 4:
        print("VISA")
else:
    print("INVALID")










