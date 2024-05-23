from tkinter import *
import customtkinter
from PIL import ImageTk, Image
from tkinter import messagebox
import re       # Import regex
import bcrypt   # Import bcrypt for password hashing

# Roman's code --------------------------------------------------------------

# 1. Create a database to store user information

import sqlite3
from tkinter import END
# End of Roman's code ----------------------------------------------------------

def load_challenge():           # Load the challenges from quizz file
    for widget in root.winfo_children():
        widget.destroy()
    import quizz_questions
    quizz_questions.main(root)  # Import the challenges from the main function of our quizz file into the current window

# Roman's code --------------------------------------------------------------

def init_db():
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL,
                 score INTEGER DEFAULT 0)''')       # Create a score field of 0, we will update user's future score to there
    conn.commit()
    conn.close()


# call the function to create the database

init_db()

# End of Roman's code ----------------------------------------------------------

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

def main_screen():
    global root, right_frame
    root = customtkinter.CTk()
    root.title("PythonBugHunt")
    root.geometry("1300x800")

    # Load background image
    bg_image = ImageTk.PhotoImage(Image.open("pics/background2.jpg"))

    # Left Frame for the background image and text
    left_frame = customtkinter.CTkFrame(master=root, width=900, height=600, corner_radius=0)
    left_frame.pack(side=LEFT, fill=Y)

    bg_label = Label(left_frame, image=bg_image)
    bg_label.place(relwidth=1, relheight=1)

    # Add text to the left frame
    text_label = customtkinter.CTkLabel(master=left_frame, text="PythonBugHunt",
                                        font=("Arial", 44), text_color="white", justify=LEFT)
    text_label.place(relx=0.1, rely=0.5, anchor=W)

    # Right Frame for the buttons
    right_frame = customtkinter.CTkFrame(master=root, width=400, height=600, corner_radius=0, fg_color="#020c15")
    right_frame.pack(side=RIGHT, fill=Y)

    show_main_buttons()

    root.mainloop()

def show_main_buttons():
    global right_frame
    # Clear the right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Add title to the right frame
    title_label = customtkinter.CTkLabel(master=right_frame, text="Get Started!", font=("Arial", 34), text_color="white")
    title_label.place(relx=0.5, rely=0.3, anchor=CENTER)

    # Add login button
    login_button = customtkinter.CTkButton(master=right_frame, text="L o g i n", font=("Arial", 20),
                                           width=200, height=50, corner_radius=25,
                                           command=show_login_form)
    login_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    # Add register button
    register_button = customtkinter.CTkButton(master=right_frame, text="R e g i s t e r", font=("Arial", 20),
                                              width=200, height=50, corner_radius=25,
                                              command=show_register_form)
    register_button.place(relx=0.5, rely=0.6, anchor=CENTER)

def show_login_form():
    global right_frame
    # Clear the right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    frame = customtkinter.CTkFrame(master=right_frame, width=400, height=500, corner_radius=0, fg_color="#020c15")
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    l1 = customtkinter.CTkLabel(master=frame, text="Welcome back", font=("Arial", 34), text_color="white")
    l1.pack(pady=10)

    my_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username",
                                      height=40, width=300,
                                      corner_radius=20,
                                      border_width=0,
                                      fg_color="#021926")
    my_entry.pack(pady=10)

    my_entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password",
                                       height=40, width=300,
                                       corner_radius=20,
                                       border_width=0,
                                       fg_color="#021926")
    my_entry2.pack(pady=10)

    login_button = customtkinter.CTkButton(master=frame, text="Continue", font=("Arial", 18),
                                           height=40, width=300, corner_radius=20,
                                           fg_color="#00A86B", text_color="white", hover_color="#009E5A", cursor="hand2",
                                           command=lambda: login_user(my_entry, my_entry2)) # call the login_user function with the username and password Entry widgets as arguments with username and password as arguments
    login_button.pack(pady=10)

    signup_label = customtkinter.CTkLabel(master=frame, text="Don't have an account?", font=("Arial", 12), text_color="white")
    signup_label.pack(pady=10)

    signup_button = customtkinter.CTkButton(master=frame, text="Sign Up", font=("Arial", 12),
                                            height=30, width=100, corner_radius=20, fg_color="white",
                                            text_color="black", hover_color="#f0f0f0", cursor="hand2",
                                            command=show_register_form)
    signup_button.pack()

    back_button = customtkinter.CTkButton(master=frame, text="Back", font=("Arial", 12),
                                          height=30, width=100, corner_radius=20, fg_color="white",
                                          text_color="black", hover_color="#f0f0f0", cursor="hand2",
                                          command=show_main_buttons)

def show_register_form():
    global right_frame
    # Clear the right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    frame = customtkinter.CTkFrame(master=right_frame, width=400, height=500, corner_radius=0, fg_color="#020c15")
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    
    l1 = customtkinter.CTkLabel(master=frame, text="Create your account", font=("Arial", 34), text_color="white")
    l1.pack(pady=10)

    user_entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Username",
                                         height=40, width=300,
                                         corner_radius=20,
                                         border_width=0,
                                         fg_color="#021926")
    user_entry1.pack(pady=10)
    # user_entry1.focus_set()  # Set focus to user_entry1 - disabled bc it removes the placeholder text "Email address", we would need a whole redesign

    user_entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*",
                                         height=40, width=300,
                                         corner_radius=20,
                                         border_width=0,
                                         fg_color="#021926")
    user_entry2.pack(pady=10)

    user_entry3 = customtkinter.CTkEntry(master=frame, placeholder_text="Confirm Password", show="*",
                                         height=40, width=300,
                                         corner_radius=20,
                                         border_width=0,
                                         fg_color="#021926")
    user_entry3.pack(pady=10)

    create_button = customtkinter.CTkButton(master=frame, text="Sign Up", font=("Arial", 18),
                                            height=40, width=300, corner_radius=20,
                                            fg_color="#00A86B", text_color="white", hover_color="#009E5A", cursor="hand2",
                                            command=lambda: create_user(user_entry1, user_entry2, user_entry3))
    create_button.pack(pady=10)

    back_button = customtkinter.CTkButton(master=frame, text="Back", font=("Arial", 12),
                                          height=30, width=100, corner_radius=20, fg_color="white",
                                          text_color="black", hover_color="#f0f0f0", cursor="hand2",
                                          command=show_main_buttons)
    back_button.pack(pady=10)


# Roman's code --------------------------------------------------------------

# 2. Create a function to create a user account

def create_user(user_entry1, user_entry2, user_entry3): # user_entry1, user_entry2, user_entry3 are Entry widgets
    username = user_entry1.get()        # get username from user entry
    password = user_entry2.get()        # get password from user entry
    confirmation = user_entry3.get()    # get password confirmation from user entry

    if password != confirmation:    # check if the passwords match
        messagebox.showinfo("Error", "Passwords don't match!")   # show an error message
        user_entry2.delete(0, END)  # clear the password Entry widget
        user_entry3.delete(0, END)  # clear the confirm password Entry widget
        return  # exit the function

    conn = sqlite3.connect('user_info.db') # connect to the database
    c = conn.cursor() # create a cursor object

    c.execute('SELECT * FROM users WHERE username = ?', (username,)) # check if the username already exists
    existing_user = c.fetchone() # fetch the result
    # valid_email_address = re.search(r"^([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})$", username)  # Check if the formatting of the email address is valid
    # strong_password = re.search(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password)

    if existing_user:   # if the username already exists
        messagebox.showinfo("Error", "Username already exists!")    # show an error message
        user_entry1.delete(0, END)  # clear the 3 widgets
        user_entry2.delete(0, END)  
        user_entry3.delete(0, END)
    elif password != confirmation:    # Show an error message and clear password fields if password confirmation not matching
        messagebox.showinfo("Error", "Passwords don't match!")
        user_entry2.delete(0, END)
        user_entry3.delete(0, END)
    # elif not valid_email_address:   # Show an error message and clear "email address" field if the email address is invalid
    #     messagebox.showinfo("Error", "Invalid email address!")
    #     user_entry1.delete(0, END)
    # elif not strong_password:       # Show an error message and clear "password" and "confirm password" fields if the password is not strong enough
    #     messagebox.showinfo("Error", "Password must be at least 8 characters long and contain at least one letter and one number!")
    #     user_entry2.delete(0, END)
    #     user_entry3.delete(0, END)  
    else:   # if the username doesn't exist
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) # hash the password
        c.execute('INSERT INTO users (username, password, score) VALUES (?, ?, ?)', (username, hashed_password, 0))  # insert the username and password into the database
        conn.commit()   # commit the changes
        messagebox.showinfo("Success", "Account created successfully! Welcome, " + username + "!")  # show a success message

        show_main_buttons() # show the main buttons
    
    conn.close()    # close the connection
    del password, confirmation, hashed_password     # Delete the password, confirmation and hashed password from memory for safety

# End of Roman's code ----------------------------------------------------------


# Morgane's code --------------------------------------------------------------

def login_user(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect('user_info.db')  # Connect to the database
    c = conn.cursor()   # Create a cursor object

    c.execute('SELECT * FROM users WHERE username = ?', (username,))    # Select the user from the database
    user = c.fetchone()                                                 # Fetch the result and store it in the user variable

    if user is None:
        messagebox.showinfo("Error", "User not found!")
        return

    stored_password = user[2]   # Get the stored password from the database
    score = user[3]

    if bcrypt.checkpw(password.encode('utf-8'), stored_password):       # Check if the password is correct
        messagebox.showinfo("Success", "Logged in successfully! Welcome, " + username + "!")
        load_challenge()  # Call user page function
    else:
        messagebox.showinfo("Error", "Incorrect password!") # Show an error message if the password is incorrect

    conn.close()    # Close the connection to database

# End of Morgane's code ----------------------------------------------------------


if __name__ == "__main__":
    main_screen()