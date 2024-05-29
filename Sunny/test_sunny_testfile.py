import customtkinter as ctk
import io
import traceback
from contextlib import redirect_stdout
import sqlite3

def run_python_code(code):
    """
    Executes Python code and captures the output.

    Args:
        code (str): The Python code to execute.

    Returns:
        str: The output of the code execution, or any errors that occurred.
    """

    # Create a String buffer to capture the output
    buffer = io.StringIO()
    try:
        # Redirect stdout to the buffer to capture print statements
        with redirect_stdout(buffer):
            exec(code, {})
    except Exception as e:
        # Capture the full traceback (error report) and add it to the buffer
        buffer.write(traceback.format_exc())
    # Get the output from the buffer and close it
    output = buffer.getvalue()
    buffer.close()
    return output

class QuizApp(ctk.CTk):
    def __init__(self, root, username):  # Initialize the QuizApp class with username and root arguments
        if root is None:            # If there is no tkinter root window, create one (used when we run this program standalone)
            root = ctk.CTk()
        self.root = root
        self.username = username

        super().__init__()
        self.title("PythonBugHunt")
        self.geometry("1300x850")

        # Create UI elements (labels, text boxes, buttons)
        # ... (same as original code) ...

        # Define a list of quiz questions with question, code, and expected output
        self.quiz_questions = [
            {
                "question": "# Fix the code to print 'Hello, World!'\nprint('Hello World')",
                "code": "print('Hello World')",
                "output": "Hello, World!\n"
            },
            {
                "question": "# Fix the code to print the sum of two numbers\na = 5\nb = 10\nprint(a, b)",
                "code": "a = 5\nb = 10\nprint(a + b)",
                "output": "15\n"
            },
            {
                "question": "# Print only the even numbers from a list:\nnumbers =[1,2,3,4,5]\nfor num in numbers:\nif num % 2 == 0:\print(num)",
                "code": """
                numbers = [1,2, 3, 4, 5]
                for num in numbers:
                    if num % 2 == 0:
                        print(num)
                """,
                "output": "2\n4\n"
            },
            {
                "question": "# Write a function that takes a number as input and returns its factorial. (Factorial of a number is the product of all positive integers less than or equal to that number)",
                "code": """
                def factorial(n):
                    if n == 0:
                        return 1
                    else:
                        return n * factorial(n-1)
                
                # Example usage:
                result = factorial(5)
                print(result)
                """,
                "output": "120\n"
            },
            {
                "question": "# Write a Python program to reverse a string. (Example: 'Hello' becomes 'olleH')",
                "code": "",  # User will write the code for this question
                "output": ""  # Output will be filled based on user code execution
            },
        ]

        # Set the initial quiz question
        self.current_question = 0
        self.set_question(self.current_question)

    def set_question(self, question_index):
        question = self.quiz_questions[question_index]
        self.code_editor.delete("0.0", "end")  # Clear code editor
        self.code_editor.insert("0.0", question["question"])  # Insert question text
        self.correct_output = question["output"]  # Store expected output

    def run_code(self):
        # Get the user's code from the Text widget
        user_code = self.code_editor.get("0.0", "end")

        # Execute the user's
