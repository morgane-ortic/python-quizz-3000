from tkinter import *
import customtkinter
from PIL import ImageTk, Image
import json
from tkinter import messagebox

# Roman's code --------------------------------------------------------------

# 1. Create a database to store user information

import sqlite3
import bcrypt
from tkinter import END

def init_db():
    conn = sqlite3.connect('user_info.db')  # connect to the database
    c = conn.cursor()   # create a cursor object
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')    # create a table to store user information
    conn.commit()   # commit the changes
    conn.close()    # close the connection


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
    my_entry.pack(pady=10)

    login_button = customtkinter.CTkButton(master=frame, text="Continue", font=("Arial", 18),
                                           height=40, width=300, corner_radius=20,
                                           fg_color="#00A86B", text_color="white", hover_color="#009E5A", cursor="hand2")
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
    back_button.pack(pady=10)

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
    username = user_entry1.get()    # get the text from the Entry widget
    password = user_entry2.get()
    confirmation = user_entry3.get()

    if password != confirmation:    # check if the passwords match
        messagebox.showinfo("Error", "Passwords don't match!")   # show an error message
        user_entry2.delete(0, END)  # clear the password Entry widget
        user_entry3.delete(0, END)  # clear the confirm password Entry widget
        return  # exit the function

    conn = sqlite3.connect('user_info.db') # connect to the database
    c = conn.cursor() # create a cursor object

    c.execute('SELECT * FROM users WHERE username = ?', (username,)) # check if the username already exists
    existing_user = c.fetchone() # fetch the result

    if existing_user:   # if the username already exists
        messagebox.showinfo("Error", "Username already exists!")    # show an error message
        user_entry1.delete(0, END)  # clear the 3 widgets
        user_entry2.delete(0, END)  
        user_entry3.delete(0, END)  
    else:   # if the username doesn't exist
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) # hash the password
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))  # insert the username and password into the database
        conn.commit()   # commit the changes
        messagebox.showinfo("Success", "Account created successfully! Welcome, " + username + "!")  # show a success message
        show_main_buttons() # show the main buttons
    
    conn.close()    # close the connection

# End of Roman's code ----------------------------------------------------------

if __name__ == "__main__":
    main_screen()