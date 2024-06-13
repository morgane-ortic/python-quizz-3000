from tkinter import *
import tkinter as tk
import json

def newquestion(name, question1, code1, output1, question2, code2, output2, question3, code3, output3):
    daten1 = {
    "question": question1.strip(),
    "code": code1.strip(),
    "output": output1.strip(),
 
}
    daten2 = {
    "question": question2.strip(),
    "code": code2.strip(),
    "output": output2.strip(),
 
}
    daten3 = {
    "question": question3.strip(),
    "code": code3.strip(),
    "output": output3.strip(),
 
}
    name = name + ".json"
    daten_liste = [daten1, daten2, daten3]
    with open( name, 'w', encoding='utf-8') as json_datei:
        json.dump(daten_liste, json_datei, ensure_ascii=False, indent=4)


def cratequestionwindow():
    window = tk.Tk()
    window.title("quizcreator")
    window.geometry("1200x1500")

  
    frame1 = tk.Frame(window, bd=2, relief=tk.GROOVE)
    frame1.pack(pady=10)

    label_name = tk.Label(frame1, text="level:")
    label_name.grid(row=0, column=0, padx=10, pady=5)
    textfeld_name = tk.Entry(frame1)
    textfeld_name.grid(row=0, column=1, padx=10, pady=5)    
    
    label_question1 = tk.Label(frame1, text="Question:")
    label_question1.grid(row=1, column=0, padx=10, pady=5)
    textfeld_question1 = tk.Text(frame1, height=5, width=100, wrap=tk.WORD, padx=5, pady=5)
    textfeld_question1.grid(row=1, column=1, padx=10, pady=5)

    label_code1 = tk.Label(frame1, text="Code")
    label_code1.grid(row=2, column=0, padx=10, pady=5)
    textfeld_code1 = tk.Text(frame1, height=5, width=100, wrap=tk.WORD, padx=5, pady=5)
    textfeld_code1.grid(row=2, column=1, padx=10, pady=5)

    label_correctoutput1 = tk.Label(frame1, text="Correct Output")
    label_correctoutput1.grid(row=3, column=0, padx=10, pady=5)
    textfeld_correctoutput1 = tk.Text(frame1, height=5, width=100, wrap=tk.WORD, padx=5, pady=5)
    textfeld_correctoutput1.grid(row=3, column=1, padx=10, pady=5)
    

    frame2 = tk.Frame(window, bd=2, relief=tk.GROOVE)
    frame2.pack(pady=10)

    label_question2 = tk.Label(frame2, text="Question:")
    label_question2.grid(row=0, column=0, padx=10, pady=5)
    textfeld_question2 = tk.Text(frame2, height=5, width=100, wrap=tk.WORD, padx=5, pady=5)
    textfeld_question2.grid(row=0, column=1, padx=10, pady=5)

    label_code2 = tk.Label(frame2, text="Code")
    label_code2.grid(row=1, column=0, padx=10, pady=5)
    textfeld_code2 = tk.Text(frame2, height=5, width=100, wrap=tk.WORD, padx=5, pady=5)
    textfeld_code2.grid(row=1, column=1, padx=10, pady=5)

    label_correctoutput2 = tk.Label(frame2, text="Correct Output")
    label_correctoutput2.grid(row=2, column=0, padx=10, pady=5)
    textfeld_correctoutput2 = tk.Text(frame2, height=5, width=100, wrap=tk.WORD, padx=5, pady=5)
    textfeld_correctoutput2.grid(row=2, column=1, padx=10, pady=5)


    frame3 = tk.Frame(window, bd=2, relief=tk.GROOVE)
    frame3.pack(pady=10)

    label_question3 = tk.Label(frame3, text="Question:")
    label_question3.grid(row=0, column=0, padx=10, pady=5)
    textfeld_question3 = tk.Text(frame3, height=5, width=100, wrap=tk.WORD, padx=5, pady=5)
    textfeld_question3.grid(row=0, column=1, padx=10, pady=5)

    label_code3 = tk.Label(frame3, text="Code")
    label_code3.grid(row=1, column=0, padx=10, pady=5)
    textfeld_code3 = tk.Text(frame3, height=5, width=100, wrap=tk.WORD, padx=5, pady=5)
    textfeld_code3.grid(row=1, column=1, padx=10, pady=5)
    
    label_correctoutput3 = tk.Label(frame3, text="Correct Output")
    label_correctoutput3.grid(row=2, column=0, padx=10, pady=5)
    textfeld_correctoutput3 = tk.Text(frame3, height=5, width=100, wrap=tk.WORD, padx=5, pady=5)
    textfeld_correctoutput3.grid(row=2, column=1, padx=10, pady=5)

    submit_button = tk.Button(window, text="save", command=lambda: newquestion(
        textfeld_name.get(), textfeld_question1.get("1.0", tk.END), textfeld_code1.get("1.0", tk.END), textfeld_correctoutput1.get("1.0", tk.END),
        textfeld_question2.get("1.0", tk.END), textfeld_code2.get("1.0", tk.END), textfeld_correctoutput2.get("1.0", tk.END),
        textfeld_question3.get("1.0", tk.END), textfeld_code3.get("1.0", tk.END), textfeld_correctoutput3.get("1.0", tk.END)
    ))
    submit_button.pack(pady=20)
    window.mainloop()
    
cratequestionwindow()
