from cs50 import get_string

# Input user for some text
text = get_string("Text: ")

# Count the number of letters, words and sentences in text
words = 1
letters = 0
sentences = 0
end = [".", "?", "!"]
for n in text:
    if n in end:
        sentences += 1
    elif n == " ":
        words += 1
    elif n.isalpha:
        letters += 1

# Applies the formula
l = letters / words * 100
s = sentences / words * 100
index = round(0.0588 * l - 0.296 * s - 15.8)

# Checks for ranges
if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")
