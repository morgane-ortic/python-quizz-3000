import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import io
import traceback
from contextlib import redirect_stdout

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

class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        tk.Text.__init__(self, *args, **kwargs)

        # Create a font for the text widget
        self.text_font = ("Consolas", 12)

        # Configure the tag for the text widget
        self.configure(font=self.text_font, bg="white", fg="black", insertbackground="black")

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PythonBugHunt")
        self.root.geometry("1600x600")

        # Create a styled window frame
        self.window_frame = tk.Frame(self.root, bg="#3399FF", bd=2, relief="groove")
        self.window_frame.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

        # Create a Text widget for code input (white background)
        self.code_editor = CustomText(self.window_frame, wrap=tk.WORD)
        self.code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 5), pady=10)

        # Create a Text widget for displaying output (black background)
        self.output_window = scrolledtext.ScrolledText(self.window_frame, font=("Consolas", 12), wrap=tk.WORD, bg="black", fg="white")
        self.output_window.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)

        # Create a styled button frame
        button_frame = tk.Frame(self.root, bg="#3399FF", bd=2, relief="groove")
        button_frame.pack(fill=tk.X, padx=1, pady=(0))

        # Create a "Prev" button
        prev_button = tk.Button(button_frame, text="Prev", command=self.prev_question, bg="#3399FF", fg="black", relief=tk.GROOVE, bd=0, font=("Arial", 14), pady=10, padx=20, compound=tk.CENTER, borderwidth=2, highlightthickness=0, highlightbackground="#3399FF", highlightcolor="#3399FF", activebackground="#FFFF00", activeforeground="black", cursor="hand2", width=8, height=1)
        prev_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a "Run" button
        run_button = tk.Button(button_frame, text="Run", command=self.run_code, bg="#3399FF", fg="black", relief=tk.GROOVE, bd=0, font=("Arial", 14), pady=10, padx=20, compound=tk.CENTER, borderwidth=2, highlightthickness=0, highlightbackground="#3399FF", highlightcolor="#3399FF", activebackground="#00FF00", activeforeground="black", cursor="hand2", width=8, height=1)
        run_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Create a "Next" button
        next_button = tk.Button(button_frame, text="Next", command=self.next_question, bg="#3399FF", fg="black", relief=tk.GROOVE, bd=0, font=("Arial", 14), pady=10, padx=20, compound=tk.CENTER, borderwidth=2, highlightthickness=0, highlightbackground="#3399FF", highlightcolor="#3399FF", activebackground="#FF0000", activeforeground="black", cursor="hand2", width=8, height=1)
        next_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Define a list of quiz questions
        self.quiz_questions = [
            {
                "question": "# Fix the code to print 'Hello, World!'\nprint('Hello World')",
                "code": "print('Hello World')",
                "output": "Hello, World!\n"
            },
            {
                "question": "# Fix the code to print the sum of two numbers\na = 5\nb = 10\nprint(a + b)",
                "code": "a = 5\nb = 10\nprint(a + b)",
                "output": "15\n"
            },
            # Add more questions here
        ]

        # Set the initial quiz question
        self.current_question = 0
        self.set_question(self.current_question)

    def set_question(self, question_index):
        question = self.quiz_questions[question_index]
        self.code_editor.delete("1.0", tk.END)
        self.code_editor.insert(tk.END, question["question"])
        self.correct_output = question["output"]

    def run_code(self):
        # Get the user's code from the Text widget
        user_code = self.code_editor.get("1.0", tk.END)

        # Execute the user's code and capture the output
        output = run_python_code(user_code)

        # Display the output in the output window
        self.output_window.delete("1.0", tk.END)
        self.output_window.insert(tk.END, output)

        # Check if the output matches the correct output
        if output.strip() == self.correct_output.strip():
            self.output_window.insert(tk.END, "\nCorrect answer!")
            # Move to the next question if available
            if self.current_question < len(self.quiz_questions) - 1:
                self.current_question += 1
                self.set_question(self.current_question)
        else:
            self.output_window.insert(tk.END, "\nIncorrect answer. Please try again.")

    def prev_question(self):
        if self.current_question > 0:
            self.current_question -= 1
            self.set_question(self.current_question)

    def next_question(self):
        if self.current_question < len(self.quiz_questions) - 1:
            self.current_question += 1
            self.set_question(self.current_question)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()