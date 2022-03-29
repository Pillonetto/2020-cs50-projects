
text = input("Text: ")
word_count = 1
letter_count = 0
sentence_count = 0

length=len(text)

for i in range(length):
    if text[i] == " ":
        word_count += 1
    elif text[i] in [".", "?", "!"]:
        sentence_count += 1
    elif ord(text[i]) in range(65, 91) or ord(text[i]) in range(97, 123):
        letter_count += 1

index_w = 100 / word_count



avg_l = letter_count * index_w
avg_s = sentence_count * index_w


coleman_liau = 0.0588 * avg_l - 0.296 * avg_s - 15.8
result = round(coleman_liau)

if result < 1:
    print("Before Grade 1")
elif result >= 16:
    print(f"Grade 16+")
else:
    print(f"Grade {result}")

print(f"{sentence_count} sentences. {word_count} words and {letter_count} letters.")

