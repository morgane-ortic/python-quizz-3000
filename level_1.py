# Define the challenges for Level 1
challenges_level_1 = [
    {
        "task": """Your task is to write a Python program (using the break statement),
that prints:
in the first line the numbers from 0 to 7,
in the second line the numbers from 10 to 17,
and in the third line the numbers from 20 to 27.

Hint: You can use nested loops! Remember that the break statement terminates the loop containing it!""",
        "output": "0 1 2 3 4 5 6 7\n10 11 12 13 14 15 16 17\n20 21 22 23 24 25 26 27\n",
        "regex": r"0 1 2 3 4 5 6 7\n10 11 12 13 14 15 16 17\n20 21 22 23 24 25 26 27",
        "code_regex": "for.*in.*range.*:.*for.*in.*range.*:.*if.*>.*:.*break",
        "solution": """
for i in range(3):
    for j in range(10):
        if j > 7:
            break
        print(i * 10 + j, end=' ')
    print()"""
    },
    {
        "task": """Python program to construct the following pattern, using a **for** loop.
Note: Don't type numbers manually. Use the loop!
1
22
333
4444
55555
666666
7777777
88888888
999999999""",
        "output": "1\n22\n333\n4444\n55555\n666666\n7777777\n88888888\n999999999\n",
        "regex": r"1\n22\n333\n4444\n55555\n666666\n7777777\n88888888\n999999999",
        "code_regex": "for\s+[a-zA-Z_][a-zA-Z0-9_]*\s+in\s+range\(\d+,\s*\d+\):",
        "solution": """for i in range(1, 10):
    print(str(i) * i)"""
    },
    {
        "task": """Python program to create the multiplication table of 6.
Print results.
Results of multiplication by 6:
6 x 1 = 6
6 x 2 = 12
6 x 3 = 18
6 x 4 = 24
6 x 5 = 30
6 x 6 = 36
6 x 7 = 42
6 x 8 = 48
6 x 9 = 54
6 x 10 = 60""",
        "output": "6 x 1 = 6\n6 x 2 = 12\n6 x 3 = 18\n6 x 4 = 24\n6 x 5 = 30\n6 x 6 = 36\n6 x 7 = 42\n6 x 8 = 48\n6 x 9 = 54\n6 x 10 = 60\n",
        "regex": r"6 x 1 = 6\n6 x 2 = 12\n6 x 3 = 18\n6 x 4 = 24\n6 x 5 = 30\n6 x 6 = 36\n6 x 7 = 42\n6 x 8 = 48\n6 x 9 = 54\n6 x 10 = 60",
        "code_regex": "for\s+[a-zA-Z_][a-zA-Z0-9_]*\s+in\s+range\(\d+,\s*\d+\):",
        "solution": """
for i in range(1, 11):
    print("6 x {} = {}".format(i, 6*i))
        """
    }
]