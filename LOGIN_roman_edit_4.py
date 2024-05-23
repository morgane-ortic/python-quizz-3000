from tkinter import *
import bcrypt
import sqlite3
import customtkinter
from tkinter import CENTER, END, messagebox, PhotoImage
from PIL import ImageTk, Image

# Function to initialize the database
def init_db():
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 username TEXT UNIQUE NOT NULL,
                 password TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Function to create a new user
def create_user(user_entry1, user_entry2, user_entry3):
    username = user_entry1.get()
    password = user_entry2.get()
    confirmation = user_entry3.get()

    if password != confirmation:
        messagebox.showinfo("Error", "Passwords don't match!")
        user_entry2.delete(0, END)
        user_entry3.delete(0, END)
        return

    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    existing_user = c.fetchone()

    if existing_user:
        messagebox.showinfo("Error", "Username already exists!")
        user_entry1.delete(0, END)
        user_entry2.delete(0, END)
        user_entry3.delete(0, END)
    else:
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        messagebox.showinfo("Success", "Account created successfully! Welcome, " + username + "!")
        show_main_buttons()
    
    conn.close()

# Function to handle user login
def login_user(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()
    
    conn = sqlite3.connect('user_info.db')
    c = conn.cursor()

    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[2].encode('utf-8')):
        messagebox.showinfo("Success", "Login successful! Welcome back, " + username + "!")
        show_main_buttons()  # Proceed to the main part of the application
    else:
        messagebox.showinfo("Error", "Invalid username or password!")
        username_entry.delete(0, END)
        password_entry.delete(0, END)

# Function to display the login form
def show_login_form():
    global right_frame
    # Clear the right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    frame = customtkinter.CTkFrame(master=right_frame, width=400, height=500, corner_radius=0, fg_color="#020c15")
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    l1 = customtkinter.CTkLabel(master=frame, text="Welcome back", font=("Arial", 34), text_color="white")
    l1.pack(pady=10)

    username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username",
                                            height=40, width=300, corner_radius=20,
                                            border_width=0, fg_color="#021926")
    username_entry.pack(pady=10)

    password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*",
                                            height=40, width=300, corner_radius=20,
                                            border_width=0, fg_color="#021926")
    password_entry.pack(pady=10)

    login_button = customtkinter.CTkButton(master=frame, text="Continue", font=("Arial", 18),
                                           height=40, width=300, corner_radius=20,
                                           fg_color="#00A86B", text_color="white", hover_color="#009E5A",
                                           cursor="hand2", command=lambda: login_user(username_entry, password_entry))
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

# Function to display the register form
def show_register_form():
    global right_frame
    # Clear the right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    frame = customtkinter.CTkFrame(master=right_frame, width=400, height=500, corner_radius=0, fg_color="#020c15")
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    l1 = customtkinter.CTkLabel(master=frame, text="Register", font=("Arial", 34), text_color="white")
    l1.pack(pady=10)

    username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Username",
                                            height=40, width=300, corner_radius=20,
                                            border_width=0, fg_color="#021926")
    username_entry.pack(pady=10)

    password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Password", show="*",
                                            height=40, width=300, corner_radius=20,
                                            border_width=0, fg_color="#021926")
    password_entry.pack(pady=10)

    confirm_password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Confirm Password", show="*",
                                                    height=40, width=300, corner_radius=20,
                                                    border_width=0, fg_color="#021926")
    confirm_password_entry.pack(pady=10)

    register_button = customtkinter.CTkButton(master=frame, text="Register", font=("Arial", 18),
                                              height=40, width=300, corner_radius=20,
                                              fg_color="#00A86B", text_color="white", hover_color="#009E5A",
                                              cursor="hand2", command=lambda: create_user(username_entry, password_entry, confirm_password_entry))
    register_button.pack(pady=10)

    back_button = customtkinter.CTkButton(master=frame, text="Back", font=("Arial", 12),
                                          height=30, width=100, corner_radius=20, fg_color="white",
                                          text_color="black", hover_color="#f0f0f0", cursor="hand2",
                                          command=show_main_buttons)
    back_button.pack(pady=10)

# Function to display the main buttons
def show_main_buttons():
    global right_frame
    # Clear the right_frame
    for widget in right_frame.winfo_children():
        widget.destroy()

    # Add your main buttons and functionality here
    frame = customtkinter.CTkFrame(master=right_frame, width=400, height=500, corner_radius=0, fg_color="#020c15")
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    main_label = customtkinter.CTkLabel(master=frame, text="Main Menu", font=("Arial", 34), text_color="white")
    main_label.pack(pady=10)

    # Add more widgets as needed

# Tkinter setup
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

# Create a frame for the right side of the window
right_frame = customtkinter.CTkFrame(master=root, width=400, height=600, corner_radius=0, fg_color="transparent")
right_frame.pack(side="right", fill="both", expand=True)

# Initialize the database
init_db()

# Show the login form on startup
show_login_form()

root.mainloop()
