import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Quiz App")
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
        self.quiz_question = "# Fix the code to print 'Hello, World!'\nprint('Hello World')"
        self.code_editor.insert(tk.END, self.quiz_question)

    def run_code(self):
        # Get the user's code from the Text widget
        user_code = self.code_editor.get("1.0", tk.END)

        # Execute the user's code and capture the output
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = output_buffer = StringIO()

        try:
            exec(user_code)
        except Exception as e:
            output_buffer.write(str(e))

        sys.stdout = old_stdout
        output = output_buffer.getvalue()

        # Display the output in the output window
        self.output_window.delete("1.0", tk.END)
        self.output_window.insert(tk.END, output)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
