import customtkinter as ctk
import io
import traceback
from contextlib import redirect_stdout
import sqlite3

# Run Python code and capture output
def run_python_code(code):
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            exec(code, {})
    except Exception:
        buffer.write(traceback.format_exc())
    output = buffer.getvalue()
    buffer.close()
    return output

class QuizApp(ctk.CTk):
    def __init__(self, root, username):
        # Initialize app window
        if root is None:
            root = ctk.CTk()
        self.root = root
        self.username = username

        super().__init__()
        self.title("PythonBugHunt")
        self.geometry("1300x850")

        # User label
        user_frame = ctk.CTkFrame(self)
        user_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.user_label = ctk.CTkLabel(user_frame, text=f"Logged in as: {self.username} | Score: {self.get_latest_score()}", font=("Arial", 18), text_color="white")
        self.user_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Code editor
        self.code_editor = ctk.CTkTextbox(self, width=650, height=700, font=("Consolas", 16), text_color="black", wrap="word", fg_color="white")
        self.code_editor.grid(row=1, column=0, padx=14, pady=10, sticky="nsew")

        # Output window
        self.output_window = ctk.CTkTextbox(self, width=600, height=700, font=("Consolas", 16), wrap="word")
        self.output_window.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Button frame
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, columnspan=2, padx=13, pady=0, sticky="ew")

        # Run button
        self.run_button = ctk.CTkButton(button_frame, text="Run", font=("Arial", 18), command=self.run_code, width=150, height=40, corner_radius=10, fg_color="green")
        self.run_button.grid(row=0, column=0, padx=5)

        # Next button
        self.next_button = ctk.CTkButton(button_frame, text="Next", font=("Arial", 18), command=self.next_question, width=150, height=40, corner_radius=10, state="disabled")
        self.next_button.grid(row=0, column=1, padx=5)

        # Main Menu button
        self.main_menu_button = ctk.CTkButton(button_frame, text="Main Menu", font=("Arial", 18), command=self.go_to_main_menu, width=150, height=40, corner_radius=10, fg_color="magenta")
        self.main_menu_button.grid(row=0, column=2, padx=5)

        # Quiz questions
        '''self.quiz_questions = [
            {
                "question": "# Fix the code to print 'Hello, World!'\nprint('Hello World'",
                "code": "print('Hello World')",
                "output": "Hello, World!\n"
            },
            {
                "question": "# Fix the code to print the sum of two numbers\na = 5\nb = 10\nprint(a b)",
                "code": "a = 5\nb = 10\nprint(a + b)",
                "output": "15\n"
            },
            {
                "question": "# Print the square of a number\nnum = 5\nprint( ** 2)",
                "code": "num = 5\nprint(num ** 2)",
                "output": "25\n"
            },
            {
                "question": "# Convert a string to uppercase\nstring = 'hello'\nprint(string.append())",
                "code": "string = 'hello'\nprint(string.upper())",
                "output": "HELLO\n"
            },
            {
                "question": "# Calculate the area of a circle with radius 3\nimport math\nradius = 3\narea = math.pi * radius ** 2\nprint(area)",
                "code": "import math\nradius = 3\narea = math.pi * radius ** 2\nprint(area)",
                "output": "28.274333882308138\n"
            },
            {
                "question": "# Reverse a list\nlist = [1, 2, 3, 4, 5]\nprint([::-1])",
                "code": "list = [1, 2, 3, 4, 5]\nprint(list[::-1])",
                "output": "[5, 4, 3, 2, 1]\n"
            },
            {
                "question": "# Check if a number is even or odd\nnum = 7\nif num % 2 == 0:\n    print('Even')\nelse:\n    print('Odd')",
                "code": "num = 7\nif num % 2 == 0:\n    print('Even')\nelse:\n    print('Odd')",
                "output": "Odd\n"
            },
            {
                "question": "# Calculate the factorial of a number\ndef factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)\n\nnum = 5\nprint(factorial(num))",
                "code": "def factorial(n):\n    if n == 0:\n        return 1\n    else:\n        return n * factorial(n-1)\n\nnum = 5\nprint(factorial(num))",
                "output": "120\n"
            },
            {
                "question": "# Count the number of vowels in a string\nstring = 'hello'\nvowels = 'aeiou'\ncount = 0\nfor char in string:\n    if char.lower() in vowels:\n        count += 1\nprint(count)",
                "code": "string = 'hello'\nvowels = 'aeiou'\ncount = 0\nfor char in string:\n    if char.lower() in vowels:\n        count += 1\nprint(count)",
                "output": "2\n"
            }
        ]'''

        # Initial question
        self.current_question = 0
        self.set_question(self.current_question)

    # Set question
    def set_question(self, question_index):
        question = self.quiz_questions[question_index]
        self.code_editor.delete("0.0", "end")
        self.code_editor.insert("0.0", question["question"])
        self.correct_output = question["output"]
        self.next_button.configure(state="disabled")
        self.output_window.delete("0.0", "end")

    # Run code
    def run_code(self):
        user_code = self.code_editor.get("0.0", "end")
        output = run_python_code(user_code)
        self.output_window.delete("0.0", "end")
        self.output_window.insert("0.0", output)

        if output.strip() == self.correct_output.strip():
            self.output_window.insert("end", "\nCorrect answer!")
            self.update_score(50)
            self.next_button.configure(state="normal")
        else:
            self.output_window.insert("end", "\nIncorrect answer. Please try again.")
            self.update_score(-5)
            self.next_button.configure(state="disabled")

    def next_question(self):
        if self.current_question < len(self.quiz_questions) - 1:
            self.current_question += 1
            self.set_question(self.current_question)

    def go_to_main_menu(self):
        print("Going back to the main menu...")
        # Add your code here for displaying the main menu

    def get_latest_score(self):
        conn = sqlite3.connect('user_info.db')
        c = conn.cursor()
        c.execute('SELECT score FROM users WHERE username = ?', (self.username,))
        score = c.fetchone()[0]
        conn.close()
        return score

    def update_score(self, points):
        conn = sqlite3.connect('user_info.db')
        c = conn.cursor()
        c.execute('UPDATE users SET score = score + ? WHERE username = ?', (points, self.username))
        conn.commit()
        conn.close()
        self.user_label.configure(text=f"Logged in as: {self.username} | Score: {self.get_latest_score()}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = QuizApp(None, username="Guest")
    app.root.mainloop()