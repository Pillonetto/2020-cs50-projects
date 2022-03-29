from cs50 import get_float

coin_counter = 0
change = 0
while not change > 0:
    change = get_float("Change owed: ")
    
change = round(change * 100)

if change == 0:
    print("0")
    exit()

while change > 25:
    change -= 25
    coin_counter += 1

while change in range(10, 24):
    change -= 10
    coin_counter += 1

while change in range(5, 9):
    change -= 5
    coin_counter += 1

while change in range(1, 4):
    coin_counter += change
    change = 0

if change == 0:
    print(f"{coin_counter}")
