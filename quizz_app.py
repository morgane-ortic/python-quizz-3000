import customtkinter as ctk  # Customtkinter library for creating the GUI
import io                    # For working with input/output streams (potentially for text handling)
import traceback             # For error handling and stack trace information
from contextlib import redirect_stdout  # For potentially capturing or redirecting program output
import sqlite3               # For working with SQLite databases (likely for storing quiz data)
import sys                   # For accessing system-specific parameters and functionalities
import json                  # For working with JSON data (potentially for loading quiz questions or settings)
import subprocess            # For potentially executing external commands or programs




# Load the challenges from quizz file
def load_menu(username):                   
    subprocess.Popen(["python3", "level_menu.py" , username])

# This code block defines a function named `run_python_code` that can be used to execute a provided Python code snippet within your application. 

def run_python_code(code):
    """
    Executes a given Python code snippet and captures its output and validity status.

    Args:
        code (str): The Python code snippet to be executed.

    Returns:
        tuple: A tuple containing the output of the code execution (str) and a boolean flag indicating if the code execution was valid (True) or encountered errors (False).
    """

    # Create a string buffer to capture the output of the code execution
    buffer = io.StringIO()

    try:
        # Redirect standard output (print statements) to the buffer
        with redirect_stdout(buffer):
            exec(code, {})
        # If no exceptions occurred, consider the code valid
        valid_code = True
    except Exception as e:
        # If an exception occurs, capture the traceback (error details)
        buffer.write(traceback.format_exc())
        # Set a flag to indicate the code execution encountered errors (not valid)
        valid_code = False

    # Get the captured output from the buffer as a string
    output = buffer.getvalue()
    # Close the buffer (release resources)
    buffer.close()

    # Return the combined output (including any errors) and the validity status
    return output, valid_code



class QuizApp(ctk.CTk):
    def __init__(self, username, level):  # ***Initialize the QuizApp class with username and root arguments***
        
        # Call the superclass's __init__ method first to ensure proper window initialization
        super().__init__() 

        self.username = username    # Pass username as parameter to the class to use it inside it
        self.level = level          # Pass level as parameter to the class to use it inside it
        self.title("PythonBugHunt")
        self.geometry("1300x850")

        # Create a frame for the username label
        user_frame = ctk.CTkFrame(self)
        user_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Create and place the username label
        self.user_label = ctk.CTkLabel(
            user_frame,
            text=f"Logged in as: {self.username} | Score: {self.get_latest_score()}",
            font=("Arial", 18),
            text_color="white"
        )
        self.user_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Create a Text widget for code input (white background)
        self.code_editor = ctk.CTkTextbox(
            self, width=650, height=700, font=("Consolas", 16), text_color="black", wrap="word", fg_color="white"
        )
        self.code_editor.grid(row=1, column=0, padx=14, pady=10, sticky="nsew")

        # Create a Text widget for displaying output (dark background)
        self.output_window = ctk.CTkTextbox(self, width=600, height=700, font=("Consolas", 16), wrap="word")
        self.output_window.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        # Create a button frame
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, columnspan=2, padx=13, pady=0, sticky="ew")

        # Create a "Run" button
        run_button = ctk.CTkButton(button_frame, text="Run", font=("Arial", 18), command=self.run_code, width=150, height=40, corner_radius=10, fg_color="green", hover_color="green")
        run_button.grid(row=0, column=0, padx=5)

        # Create a "Next" button (initially disabled)
        self.next_button = ctk.CTkButton(button_frame, text="Next", font=("Arial", 18), command=self.next_question, width=150, height=40, corner_radius=10, state="disabled", fg_color="grey")
        self.next_button.grid(row=0, column=1, padx=5)

        # Create a "quit" button
        quit_button = ctk.CTkButton(
            button_frame, text="Quit", font=("Arial", 18), command=self.quit_question, width=150, height=40, corner_radius=10, fg_color="red", hover_color="red"
        )
        quit_button.grid(row=0, column=3, padx=5)

    
        # Construct the filename based on the selected level
        challenge_filename = f"{level}.json"
        # Open the JSON file and load the data
        with open(challenge_filename, 'r') as f:
            self.quiz_questions = json.load(f)

        # Set the initial quiz question
        self.current_question = 0
        self.set_question(self.current_question)

        # Initialize the highscore database for the given level
        self.init_highscore_db()

    def init_highscore_db(self):
        self.highscore_db_name = f'highscore_{self.level}.db'
        conn = sqlite3.connect(self.highscore_db_name)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS highscore (
                username TEXT NOT NULL,
                highscore INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()


    def set_question(self, question_index):
        question = self.quiz_questions[question_index]
        self.code_editor.delete("0.0", "end")
        self.code_editor.insert("0.0", question["question"])        # add the question field to left window
        self.code_editor.insert("end", "\n\n" + question["code"])   # add the code field to left window
        self.correct_output = question["output"]                    # import the expected output
        self.next_button.configure(state="disabled", fg_color="grey")  # ***Disable the "Next" button***

    def run_code(self):
        # Get the user's code from the Text widget
        user_code = self.code_editor.get("0.0", "end")

        # Execute the user's code and capture the output
        output, valid_code = run_python_code(user_code)

        # Define the 'tag_green' and 'tag_red' tags
        self.output_window.tag_config("tag_green", foreground="green2")
        self.output_window.tag_config("tag_red", foreground="red")
        self.output_window.tag_config("tag_orange", foreground="orange")

        # Display the output in the output window
        self.output_window.delete("0.0", "end")
        # If code is valid, display the output normally
        if valid_code is True:
            self.output_window.insert("0.0", output)
        # If entered code isn't valid, display the output (error traceback) in orange
        else:
            self.output_window.insert("0.0", output, "tag_orange")

        # Check if the output matches the correct output
        if output.strip() == self.correct_output.strip():
            self.output_window.insert("end", "\nCorrect answer!", "tag_green")
            self.update_score(50)  # Increase score by 50 for a correct answer
            self.next_button.configure(state="normal", fg_color="blue", hover_color="blue")  # *Enable the "Next" button*
        else:
            self.output_window.insert("end", "\nIncorrect answer. Please try again.", "tag_red")
            self.update_score(-5)  # Decrease score by 5 for an incorrect answer

    '''def prev_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.set_question(self.current_question)'''

    def next_question(self):
        if self.current_question < len(self.quiz_questions) - 1:
            self.current_question += 1
            self.set_question(self.current_question)
            self.output_window.delete("0.0", "end")  # Clear the right screen
            self.next_button.configure(state="disabled")  # Disable the "Next" button

    def quit_question(self):
        self.transfer_and_reset_score()
        load_menu(self.username)
        self.destroy()
# Ramon's code       
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

    def update_score(self, points):
        conn = sqlite3.connect('user_info.db')
        c = conn.cursor()
        c.execute('UPDATE users SET score = score + ? WHERE username = ?', (points, self.username))
        conn.commit()
        conn.close()
        # Update the label to reflect the new score
        self.user_label.configure(text=f"Logged in as: {self.username} | Score: {self.get_latest_score()}")

    def transfer_and_reset_score(self):
        conn_user_info = sqlite3.connect('user_info.db')
        conn_highscore = sqlite3.connect(self.highscore_db_name)

        c_user_info = conn_user_info.cursor()
        c_highscore = conn_highscore.cursor()

        # Get the current score
        c_user_info.execute('SELECT score FROM users WHERE username = ?', (self.username,))
        score = c_user_info.fetchone()[0]

        # Insert the current score into the level-specific highscore.db
        c_highscore.execute('INSERT INTO highscore (username, highscore) VALUES (?, ?)', (self.username, score))

        # Reset the score in user_info.db
        c_user_info.execute('UPDATE users SET score = 0 WHERE username = ?', (self.username,))

        conn_user_info.commit()
        conn_highscore.commit()

        conn_user_info.close()
        conn_highscore.close()
# Ramon and Morgane's code
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  # Set the appearance mode to dark
    imported_username = sys.argv[1] if len(sys.argv) > 1 else "Guest"  # Get the username from the command-line arguments, or use "Guest" as default value if no username is passed
    imported_level = sys.argv[2] if len(sys.argv) > 2 else "lvl1" # Get the level from the command-line arguments, or use "lvl1" as default value if no level is passed
    app = QuizApp(username = imported_username, level = imported_level)  # Create an instance of the QuizApp class with a username
    app.mainloop()  # Start the Tkinter event loop for the root window of the QuizApp instance