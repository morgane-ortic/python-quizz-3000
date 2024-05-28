from tkinter import *
#import customtkinter
from PIL import ImageTk, Image
from tkinter import messagebox 
import tkinter as tk
import sqlite3

def createTableQuestion():
    conn = sqlite3.connect('user_questions.db')
    c = conn.cursor()
    c.execute( '''
                CREATE TABLE IF NOT EXISTS Question(
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 quiz_question TEXT NOT NULL,
                 correct_output TEXT NOT NULL)
              ''')
    conn.commit()
    conn.close()

createTableQuestion()


def newquestion(name, question, correctoutput):
    print(name, question, correctoutput)
    conn = sqlite3.connect('user_questions.db')
    cursor = conn.cursor()
    insert_query = '''
    INSERT INTO Question (name, quiz_question, correct_output)
    VALUES (?, ?, ?)
    '''
    
    try:
        cursor.execute(insert_query, (name, question, correctoutput))
        conn.commit()
        print("Successful")
    except sqlite3.Error as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        # Verbindung zur Datenbank schließen
        conn.close()    

def editquestion(id, name, question, correctoutput):
    print(id, name, question, correctoutput)
    return 0

def cratequestionwindow():
    print("createquestionwindow")
    window = tk.Tk()
    window.title("quizcreator")
    window.geometry("1300x800")
    print("allquestion")

    label_name = tk.Label(window, text="Name:")
    label_name.pack(pady=10)
    textfeld_name = tk.Entry(window)
    textfeld_name.pack(pady=10)    

    label_question = tk.Label(window, text="Question:")
    label_question.pack(pady=10)
    textfeld_question = tk.Entry(window)
    textfeld_question.pack(pady=10)

    label_correctoutput = tk.Label(window, text="Correct Output")
    label_correctoutput.pack(pady=10)
    textfeld_correctoutput = tk.Entry(window)
    textfeld_correctoutput.pack(pady=10)

    button_commit = tk.Button(window, text="commit", command=lambda: newquestion(name=textfeld_name.get(), question=textfeld_question.get(), correctoutput=textfeld_correctoutput.get() ))
    button_commit.pack(pady=10)
    window.mainloop()

def editquestinwindow(id):
    print("createquestionwindow")
    window = tk.Tk()
    window.title("quizcreator")
    window.geometry("1300x800")
    print("allquestion")

    label_name = tk.Label(window, text="Name:")
    label_name.pack(pady=10)
    textfeld_name = tk.Entry(window)
    textfeld_name.pack(pady=10)    

    label_question = tk.Label(window, text="Question:")
    label_question.pack(pady=10)
    textfeld_question = tk.Entry(window)
    textfeld_question.pack(pady=10)

    label_correctoutput = tk.Label(window, text="Correct Output")
    label_correctoutput.pack(pady=10)
    textfeld_correctoutput = tk.Entry(window)
    textfeld_correctoutput.pack(pady=10)

    button_save = tk.Button(window, text="save", command=lambda: editquestion(id=id, name=textfeld_name.get(), question=textfeld_question.get(), correctoutput=textfeld_correctoutput.get() ))
    button_save.pack(pady=10)
    window.mainloop()

def allquestionwinow():
    conn = sqlite3.connect('user_questions.db')
    c = conn.cursor()
    c.execute('SELECT id, name FROM Question')
    allquest = c.fetchall()
    conn.close()
    x = 0
    window = tk.Tk()
    window.title("quizcreator")
    window.geometry("1300x800")
    button_commit_list = []
    label_name_list = []
    while x< allquest.__len__():
        label_name = tk.Label(window, text= allquest[x][1])
        label_name_list.append(label_name)
        label_name_list[x].pack(pady=10)
        button = tk.Button(window, text="edit", command= lambda: editquestinwindow(allquest[x][0]))
        button_commit_list.append(button)
        button_commit_list[x].pack(pady=10)
        print(x)
        x = x+1
    
    window.mainloop()
    # liste aus label mit den namen der question
    # neben dem labels folgende buttons 
        # edit, delete
            # mybe all that delete go to archiv
    return 0

def main_screen():
    window = tk.Tk()
    window.title("quizcreator")
    window.geometry("1300x800")
    create_button = tk.Button(window, text="Create", command=cratequestionwindow)
    create_button.pack()
    edit_button = tk.Button(window, text="Edit", command=allquestionwinow)
    edit_button.pack()
    window.mainloop() 


if __name__ == "__main__":
    main_screen()
