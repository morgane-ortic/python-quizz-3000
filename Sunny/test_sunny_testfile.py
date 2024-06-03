import customtkinter as ctk
import io
import traceback
from contextlib import redirect_stdout
import sqlite3
import sys
import json
import subprocess

def load_menu(username):                   # Load the challenges from quizz file
    subprocess.Popen(["python3", "level_menu.py" , username])

def run_python_code(code):
    """
    This function executes the given Python code and captures the output, including any exceptions and tracebacks.
    It returns the captured output as a string and a boolean value indicating if the code is valid or not.
    """
    buffer = io.StringIO()
    try:
        with redirect_stdout(buffer):
            exec(code, {})
        valid_code = True
    except Exception:
        buffer.write(traceback.format_exc())
        valid_code = False
    output = buffer.getvalue()
    buffer.close()
    return output, valid_code

class QuizApp(ctk.CTk):
    def __init__(self, username, level):
        """
        This is the constructor for the QuizApp class. It initializes the application window and its components.
        """
        super().__init__()
        self.username = username
        self.level = level
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

        # Create a "Run" button
        run_button = ctk.CTkButton(button_frame, text="Run", font=("Arial", 18), command=self.run_code, width=150, height=40, corner_radius=10, fg_color="green")
        run_button.grid(row=0, column=0, padx=5)

        # Create a "Next" button (initially disabled)
        self.next_button = ctk.CTkButton(button_frame, text="Next", font=("Arial", 18), command=self.next_question, width=150, height=40, corner_radius=10, state="disabled")
        self.next_button.grid(row=0, column=1, padx=5)

        ''' # Create a "Main Menu" button
        main_menu_button = ctk.CTkButton(button_frame, text="Main Menu", font=("Arial", 18), width=150, height=40, corner_radius=10, fg_color="magenta")
        main_menu_button.grid(row=0, column=2, padx=5)'''

        # Create a "quit" button
        quit_button = ctk.CTkButton(
            button_frame, text="Quit", font=("Arial", 18), command=self.quit_question, width=150, height=40, corner_radius=10, fg_color="magenta"
        )
        quit_button.grid(row=0, column=2, padx=5)

        # Load the quiz questions from a JSON file based on the selected level
        challenge_filename = f"{level}.json"
        with open(challenge_filename, 'r') as f:
            self.quiz_questions = json.load(f)

        # Set the initial quiz question
        self.current_question = 0
        self.set_question(self.current_question)

    def set_question(self, question_index):
        """
        This method sets the current quiz question in the code editor and output window.
        It also disables the "Next" button.
        """
        question = self.quiz_questions[question_index]
        self.code_editor.delete("0.0", "end")
        self.code_editor.insert("0.0", question["question"])
        self.correct_output = question["output"]
        self.next_button.configure(state="disabled")  # Disable the "Next" button

    def run_code(self):
        """
        This method runs the user's code, captures the output, and compares it with the correct output.
        It updates the output window with the user's output and provides feedback.
        It also enables/disables the "Next" button based on the user's answer.
        """
        user_code = self.code_editor.get("0.0", "end")
        output, valid_code = run_python_code(user_code)

        # Configure text tags for different output colors
        self.output_window.tag_config("tag_green", foreground="green2")
        self.output_window.tag_config("tag_red", foreground="red")
        self.output_window.tag_config("tag_orange", foreground="orange")

        # Display the output in the output window
        self.output_window.delete("0.0", "end")
        if valid_code:
            self.output_window.insert("0.0", output)
        else:
            self.output_window.insert("0.0", output, "tag_orange")

        # Check if the output matches the correct output
        if output.strip() == self.correct_output.strip():
            self.output_window.insert("end", "\nCorrect answer!", "tag_green")
            self.next_button.configure(state="normal")  # Enable the "Next" button
        else:
            self.output_window.insert("end", "\nIncorrect answer. Please try again.", "tag_red")
            self.next_button.configure(state="disabled")  # Disable the "Next" button

    def next_question(self):
        """
        This method moves to the next quiz question if there are more questions available.
        """
        if self.current_question < len(self.quiz_questions) - 1:
            self.current_question += 1
            self.set_question(self.current_question)

    def quit_question(self):
        self.transfer_and_reset_score()
        load_menu(self.username)
        self.destroy()

    def get_latest_score(self):
        """
        This method retrieves the user's latest score from the database.
        """
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
                score = 0
            conn.close()
        except sqlite3.Error:
            score = 0
        return score

if __name__ == "__main__":
    """
    This is the entry point of the program.
    It sets the appearance mode to dark, creates an instance of the QuizApp class with a default username and level,
    and starts the Tkinter event loop for the root window of the QuizApp instance.
    """
    ctk.set_appearance_mode("dark")
    imported_username = sys.argv[1] if len(sys.argv) > 1 else "Guest"
    imported_level = sys.argv[2] if len(sys.argv) > 2 else "lvl1"
    app = QuizApp(username=imported_username, level=imported_level)
    app.mainloop()
