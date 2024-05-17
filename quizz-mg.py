import tkinter as tk
import sys
import io
import re

from level_1 import challenges_level_1
from level_2 import challenges_level_2

# Initialize variables
current_level = 1
current_challenge = 0
score = 0
attempted = set()
max_score_level_1 = len(challenges_level_1) * 2
passing_score = 0.9 * max_score_level_1

# Define the function to execute user code
def execute_code(user_code):
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    try:
        exec(user_code)
    except Exception as e:
        buffer.write(f"Error: {e}")
    sys.stdout = old_stdout
    return buffer.getvalue()

# Define the function to validate the output
def validate_code(level, challenge, user_output, user_code):
    challenges = challenges_level_1 if level == 1 else challenges_level_2
    expected_output = challenges[challenge]["output"].strip()
    user_output = user_output.strip()

    # Normalize line endings and remove trailing spaces
    user_output_lines = [line.strip() for line in user_output.splitlines()]
    expected_output_lines = [line.strip() for line in expected_output.splitlines()]

    # Rejoin lines to maintain structure
    normalized_user_output = '\n'.join(user_output_lines)
    normalized_expected_output = '\n'.join(expected_output_lines)

    # Debugging prints
    print(f"Normalized Expected output: '{normalized_expected_output}'")
    print(f"Normalized User output: '{normalized_user_output}'")

    # Compare normalized output directly with expected output
    # and check that the basic syntax of the code is correct
    # for that we compare it with the regex_code from the challenge dictionary, which looks for key parts that need to be in the code
    if normalized_expected_output == normalized_user_output and re.search(challenges[challenge]["code_regex"], user_code, re.DOTALL):
        return "Correct!"
    else:
        # Show detailed comparison for debugging
        for i, (expected_line, user_line) in enumerate(zip(expected_output_lines, user_output_lines)):
            if expected_line != user_line:
                print(f"Line {i+1} mismatch:")
                print(f"Expected: '{expected_line}'")
                print(f"Got:      '{user_line}'")
                break
        return f"Incorrect. Expected output:\n{normalized_expected_output}\nYour output:\n{normalized_user_output}"



# Define the function to present the challenge
def present_challenge(level, challenge):
    challenges = challenges_level_1 if level == 1 else challenges_level_2
    task_label.config(text=challenges[challenge]["task"])
    code_entry.delete("1.0", tk.END)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.config(state=tk.DISABLED)
    if challenge == len(challenges) - 1:
        end_button.pack()
    else:
        end_button.pack_forget()

# Define the function to handle the submission
def submit_solution():
    global score
    user_code = code_entry.get("1.0", tk.END)
    user_output = execute_code(user_code)
    result = validate_code(current_level, current_challenge, user_output, user_code)
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, result)
    output_text.config(state=tk.DISABLED)
    if "Correct!" in result:
        if current_challenge not in attempted:
            if current_level == 1:
                score += 2
            else:
                score += 5
            attempted.add(current_challenge)

# Define the function to show the final score and transition to Level 2 if the score is sufficient
def show_final_score():
    global current_level, current_challenge, score, attempted
    final_score_window = tk.Toplevel(root)
    final_score_window.title("Final Score")
    
    if current_level == 1 and score >= passing_score:
        score_label = tk.Label(final_score_window, text=f"Your final score is: {score} points\nCongratulations for scoring more than 90%! Click Next to go to Challenge Level 2.")
        next_button = tk.Button(final_score_window, text="Next", command=transition_to_level_2)
        next_button.pack(pady=10)
    elif current_level == 1:
        score_label = tk.Label(final_score_window, text=f"Your final score is: {score} points\nYou Failed.")
    else:
        score_label = tk.Label(final_score_window, text=f"Your final score is: {score} points")
        
    score_label.pack(pady=20)

# Define the function to transition to Level 2
def transition_to_level_2():
    global root, current_level, current_challenge, score, attempted
    current_level = 2
    current_challenge = 0
    score = 0
    attempted = set()
    for widget in root.winfo_children():
        widget.destroy()
    create_ui_elements()
    present_challenge(current_level, current_challenge)

# Define the function to go to the next challenge
def next_challenge():
    global current_challenge
    challenges = challenges_level_1 if current_level == 1 else challenges_level_2
    if current_challenge < len(challenges) - 1:
        current_challenge += 1
        present_challenge(current_level, current_challenge)

# Define the function to go to the previous challenge
def prev_challenge():
    global current_challenge
    if current_challenge > 0:
        current_challenge -= 1
        present_challenge(current_level, current_challenge)

# Create the UI elements
def create_ui_elements():
    global task_label, code_entry, submit_button, output_text, prev_button, next_button, end_button

    task_label = tk.Label(root, text="", wraplength=600, justify="left")
    task_label.pack(pady=10)

    code_entry = tk.Text(root, height=15, width=80)
    code_entry.pack(pady=10)

    submit_button = tk.Button(root, text="Submit", command=submit_solution)
    submit_button.pack(pady=10)

    output_text = tk.Text(root, height=10, width=80, state=tk.DISABLED)
    output_text.pack(pady=10)

    prev_button = tk.Button(root, text="Previous", command=prev_challenge)
    prev_button.pack(side=tk.LEFT, padx=20)

    next_button = tk.Button(root, text="Next", command=next_challenge)
    next_button.pack(side=tk.RIGHT, padx=20)

    end_button = tk.Button(root, text="END", command=show_final_score)
    end_button.pack_forget()

# Create the main window
root = tk.Tk()
root.title("Coding Challenge")

# Present the first challenge
create_ui_elements()
present_challenge(current_level, 0)

# Start the main event loop
root.mainloop()