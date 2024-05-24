import customtkinter as ctk
import io
import traceback
from contextlib import redirect_stdout
from customtkinter import CTkLabel


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
    def __init__(self, root=None):  # Initialize the QuizApp class, with an additional root window argument allowing the use of an existing Tkinter window
        if root is None:            # If there is no tkinter root window, create one (used when we run this program standalone)
            root = ctk.CTk()
        self.root = root

        super().__init__()
        self.title("PythonBugHunt")
        self.geometry("1300x800")

        # Create a Text widget for code input (white background)
        self.code_editor = ctk.CTkTextbox(self, width=650, height=700, font=("Consolas", 16,),text_color="black", wrap="word", fg_color="white")
        self.code_editor.grid(row=0, column=0, padx=14, pady=10, sticky="nsew")

        # Create a Text widget for displaying output (dark background)
        self.output_window = ctk.CTkTextbox(self, width=600, height=700, font=("Consolas", 16), wrap="word")
        self.output_window.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Create a button frame
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=1, column=0, columnspan=2, padx=13, pady=0, sticky="ew")

        # Create a "Prev" button
        prev_button = ctk.CTkButton(button_frame, text="Prev", font=("Arial",18), command=self.prev_question, width=150, height=40, corner_radius=10)
        prev_button.grid(row=0, column=0, padx=0)

        # Create a "Run" button
        run_button = ctk.CTkButton(button_frame, text="Run", font=("Arial",18), command=self.run_code, width=150, height=40, corner_radius=10, fg_color="green")
        run_button.grid(row=0, column=1, padx=5)

        # Create a "Next" button
        next_button = ctk.CTkButton(button_frame, text="Next", font=("Arial",18), command=self.next_question, width=150, height=40, corner_radius=10)
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

if __name__ == "__main__":
    ctk.set_appearance_mode("dark") # Set the appearance mode to dark
    app = QuizApp()                 # Create an instance of the QuizApp class
    app.root.mainloop()             # Start the Tkinter event loop for the root window of the QuizApp instance
