from cs50 import get_int
def build(h, height):
    print(" " * (height - h), end = "")
    print("#" * h, end = "  ")
    print("#" * h)

height = 0

while height < 1 or height > 8:
    height = get_int("Height: ")

h = 1
while h <= height:
    build(h, height)
    h+=1




