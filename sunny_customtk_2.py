import customtkinter as ctk
import io
import traceback
from contextlib import redirect_stdout
import sqlite3
import sys          # Import sys to access passed arguments


def run_python_code(code):
    # Create a string buffer to capture the output
    buffer = io.StringIO()
    try:
        # Redirect stdout to the buffer
        with redirect_stdout(buffer):
            exec(code, {})
    except Exception as e:
        # Capture the full traceback and add it to the buffer
        buffer.write(traceback.format_exc())
    # Get the output from the buffer
    output = buffer.getvalue()
    buffer.close()
    return output

class QuizApp(ctk.CTk):
    def __init__(self, username):  # Initialize the QuizApp class with username and root arguments

        super().__init__()
        self.username = username
        self.title("PythonBugHunt")
        self.geometry("1300x840")

        # Create a frame for the username label
        user_frame = ctk.CTkFrame(self)
        user_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Create and place the username label
        self.user_label = ctk.CTkLabel(user_frame, text=f"Logged in as: {self.username} | Score: {self.get_latest_score()}", font=("Arial", 18), text_color="white")
        self.user_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Create a Text widget for code input (white background)
        self.code_editor = ctk.CTkTextbox(self, width=650, height=700, font=("Consolas", 16), text_color="black", wrap="word", fg_color="white")
        self.code_editor.grid(row=1, column=0, padx=14, pady=10, sticky="nsew")

        # Create a Text widget for displaying output (dark background)
        self.output_window = ctk.CTkTextbox(self, width=600, height=700, font=("Consolas", 16), wrap="word")
        self.output_window.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Create a button frame
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, columnspan=2, padx=13, pady=0, sticky="ew")

        # Create a "Prev" button
        prev_button = ctk.CTkButton(button_frame, text="Prev", font=("Arial", 18), command=self.prev_question, width=150, height=40, corner_radius=10)
        prev_button.grid(row=0, column=0, padx=0)

        # Create a "Run" button
        run_button = ctk.CTkButton(button_frame, text="Run", font=("Arial", 18), command=self.run_code, width=150, height=40, corner_radius=10, fg_color="green")
        run_button.grid(row=0, column=1, padx=5)

        # Create a "Next" button
        next_button = ctk.CTkButton(button_frame, text="Next", font=("Arial", 18), command=self.next_question, width=150, height=40, corner_radius=10)
        next_button.grid(row=0, column=2, padx=5)

        # Define a list of quiz questions
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
            }
        ]

        # Set the initial quiz question
        self.current_question = 0
        self.set_question(self.current_question)

    def set_question(self, question_index):
        question = self.quiz_questions[question_index]
        self.code_editor.delete("0.0", "end")
        self.code_editor.insert("0.0", question["question"])
        self.correct_output = question["output"]

    def run_code(self):
        # Get the user's code from the Text widget
        user_code = self.code_editor.get("0.0", "end")

        # Execute the user's code and capture the output
        output = run_python_code(user_code)

        # Display the output in the output window
        self.output_window.delete("0.0", "end")
        self.output_window.insert("0.0", output)

        # Check if the output matches the correct output
        if output.strip() == self.correct_output.strip():
            self.output_window.insert("end", "\nCorrect answer!")
            # Move to the next question if available
            if self.current_question < len(self.quiz_questions) - 1:
                self.current_question += 1
                self.set_question(self.current_question)
        else:
            self.output_window.insert("end", "\nIncorrect answer. Please try again.")

    def prev_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.set_question(self.current_question)

    def next_question(self):
        if self.current_question < len(self.quiz_questions) - 1:
            self.current_question += 1
            self.set_question(self.current_question)
    
    def get_latest_score(self):
        try:
            conn = sqlite3.connect('user_info.db')
            c = conn.cursor()
            try:
                c.execute('SELECT score FROM users WHERE username = ?', (self.username,))
                try:
                    score = c.fetchone()[0]
                except TypeError:
                    score = 0
            except sqlite3.OperationalError:
                score = 0  # Return 0 if the 'users' table doesn't exist
            conn.close()
        except sqlite3.Error:
            score = 0  # Return 0 if the database connection fails
        return score

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Set the appearance mode to dark
    imported_username = sys.argv[1] if len(sys.argv) > 1 else "Guest"  # Get the username from the command-line arguments, or use "Guest" as a default value if no username is passed
    imported_level = sys.argv[2] if len(sys.argv) > 2 else 1 # Get the level from the command-line arguments, or use 0 as a default value if no level is passed
    app = QuizApp(username = imported_username, level = imported_level)  # Create an instance of the QuizApp class with a username
    app.mainloop()  # Start the Tkinter event loop for the root window of the QuizApp instance
