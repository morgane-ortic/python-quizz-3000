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

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PythonBugHunt")
        self.root.geometry("1600x600")

        # Set the default theme to dark mode
        self.root.config(bg="#333333")

        # Create a Frame to hold the two windows
        window_frame = tk.Frame(self.root, bg="#333333")
        window_frame.pack(fill=tk.BOTH, expand=True)

        # Create a Text widget for code input
        self.code_editor = scrolledtext.ScrolledText(window_frame, font=("Consolas", 12), wrap=tk.WORD, bg="#333333", fg="white")
        self.code_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Text widget for displaying output
        self.output_window = scrolledtext.ScrolledText(window_frame, font=("Consolas", 12), wrap=tk.WORD, bg="#333333", fg="white")
        self.output_window.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create a Frame for the buttons
        button_frame = tk.Frame(self.root, bg="#333333")
        button_frame.pack(fill=tk.X)

        # Create a "Run" button
        run_button = tk.Button(button_frame, text="Run", command=self.run_code, bg="#4CAF50", fg="white", relief=tk.RAISED)
        run_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Set the quiz question
        self.quiz_question = "# Fix the code to print 'Hello, World!' 5 times\nfor i in range(5):\n    print('Hello World', i)"
        self.correct_output = "Hello World 0\nHello World 1\nHello World 2\nHello World 3\nHello World 4\n"
        self.code_editor.insert(tk.END, self.quiz_question)

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
        else:
            self.output_window.insert(tk.END, "\nIncorrect answer. Please try again.")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
