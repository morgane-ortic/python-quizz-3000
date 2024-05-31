from tkinter import *
#import customtkinter
#from PIL import ImageTk, Image
from tkinter import messagebox 
import tkinter as tk
import json
import os


def newquestion(level1, question1, code1, output1, question2, code2, output2, question3, code3, output3):
    print(level1, question1, output1, question2, output2,  question3, output3)
    daten1 = {
    "question": question1,
    "code": code1,
    "output": output1,
 
}
    daten2 = {
    "question": question2,
    "code": code2,
    "output": output2,
 
}
    daten3 = {
    "question": question3,
    "code": code3,
    "output": output3,
 
}
    name = "lvl" + level1 + ".json"
    daten_liste = [daten1, daten2, daten3]
    with open( name, 'w', encoding='utf-8') as json_datei:
        json.dump(daten_liste, json_datei, ensure_ascii=False, indent=4)
    
def cratequestionwindow():
    print("createquestionwindow")
    window = tk.Tk()
    window.title("quizcreator")
    window.geometry("1300x800")

    label_level1 = tk.Label(window, text="level:")
    label_level1.pack(pady=10)
    textfeld_level1 = tk.Entry(window)
    textfeld_level1.pack(pady=10)    
    
    label_question1 = tk.Label(window, text="Question:")
    label_question1.pack(pady=10)
    textfeld_question1 = tk.Entry(window)
    textfeld_question1.pack(pady=10)

    label_code1 = tk.Label(window, text="code")
    label_code1.pack(pady=10)
    textfeld_code1 = tk.Entry(window)
    textfeld_code1.pack(pady=10)

    label_correctoutput1 = tk.Label(window, text="Correct Output")
    label_correctoutput1.pack(pady=10)
    textfeld_correctoutput1 = tk.Entry(window)
    textfeld_correctoutput1.pack(pady=10)
    
   
    label_question2 = tk.Label(window, text="Question:")
    label_question2.pack(pady=10)
    textfeld_question2 = tk.Entry(window)
    textfeld_question2.pack(pady=10)

    label_code2 = tk.Label(window, text="code")
    label_code2.pack(pady=10)
    textfeld_code2 = tk.Entry(window)
    textfeld_code2.pack(pady=10)

    label_correctoutput2 = tk.Label(window, text="Correct Output")
    label_correctoutput2.pack(pady=10)
    textfeld_correctoutput2 = tk.Entry(window)
    textfeld_correctoutput2.pack(pady=10)


    label_question3 = tk.Label(window, text="Question:")
    label_question3.pack(pady=10)
    textfeld_question3 = tk.Entry(window)
    textfeld_question3.pack(pady=10)

    label_code3 = tk.Label(window, text="code")
    label_code3.pack(pady=10)
    textfeld_code3 = tk.Entry(window)
    textfeld_code3.pack(pady=10)
    
    label_correctoutput3 = tk.Label(window, text="Correct Output")
    label_correctoutput3.pack(pady=10)
    textfeld_correctoutput3 = tk.Entry(window)
    textfeld_correctoutput3.pack(pady=10)

    submit_button = tk.Button(window, text="Daten speichern", command=lambda: newquestion(
        textfeld_level1.get(), textfeld_question1.get(), textfeld_code1.get(), textfeld_correctoutput1.get(),
        textfeld_question2.get(), textfeld_code2.get(), textfeld_correctoutput2.get(),
        textfeld_question3.get(), textfeld_code3.get(), textfeld_correctoutput3.get()
    ))
    submit_button.pack(pady=20)
    window.geometry("1600x1200")
    window.mainloop()


def main_screen():
    window = tk.Tk()
    window.title("quizcreator")
    window.geometry("1300x800")
    create_button = tk.Button(window, text="Create", command=cratequestionwindow)
    create_button.pack()
    window.mainloop() 


if __name__ == "__main__":
    main_screen()
