from tkinter import *
import tkinter as tk
import json

def newquestion(level1, question1, code1, output1, question2, code2, output2, question3, code3, output3):
    print(level1, question1, output1, question2, output2,  question3, output3)
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
    name = "lvl" + level1 + ".json"
    daten_liste = [daten1, daten2, daten3]
    with open( name, 'w', encoding='utf-8') as json_datei:
        json.dump(daten_liste, json_datei, ensure_ascii=False, indent=4)


def cratequestionwindow():
    def change_lvl():
        print("changelvl")
        print("|" + textfeld_level1.get() +"|")
        print(type(textfeld_level1.get()))
        if type(textfeld_level1.get()) == str:
            print("textfieldlvl ist eine Zeichenkette")
        else:
            print("x ist keine Zeichenkette")
        if isinstance(textfeld_level1.get(), int):
            lvl = textfeld_level1.get().strip + 1
            textfeld_level1.delete('0', 'end')
            textfeld_level1.insert(lvl)
            newquestion(
        textfeld_level1.get(), textfeld_question1.get("1.0", tk.END), textfeld_code1.get("1.0", tk.END), textfeld_correctoutput1.get("1.0", tk.END),
        textfeld_question2.get("1.0", tk.END), textfeld_code2.get("1.0", tk.END), textfeld_correctoutput2.get("1.0", tk.END),
        textfeld_question3.get("1.0", tk.END), textfeld_code3.get("1.0", tk.END), textfeld_correctoutput3.get("1.0", tk.END)
    )
        else:
            lvl = int(textfeld_level1.get().strip()) + 1
            textfeld_level1.delete('0', 'end')
            textfeld_level1.insert(lvl)
            newquestion(
        textfeld_level1.get(), textfeld_question1.get("1.0", tk.END), textfeld_code1.get("1.0", tk.END), textfeld_correctoutput1.get("1.0", tk.END),
        textfeld_question2.get("1.0", tk.END), textfeld_code2.get("1.0", tk.END), textfeld_correctoutput2.get("1.0", tk.END),
        textfeld_question3.get("1.0", tk.END), textfeld_code3.get("1.0", tk.END), textfeld_correctoutput3.get("1.0", tk.END)
    )

    window = tk.Tk()
    window.title("quizcreator")
    window.geometry("1200x1500")

  
    frame1 = tk.Frame(window, bd=2, relief=tk.GROOVE)
    frame1.pack(pady=10)

    label_level1 = tk.Label(frame1, text="level:")
    label_level1.grid(row=0, column=0, padx=10, pady=5)
    textfeld_level1 = tk.Entry(frame1)
    textfeld_level1.grid(row=0, column=1, padx=10, pady=5)    
    
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
        textfeld_level1.get(), textfeld_question1.get("1.0", tk.END), textfeld_code1.get("1.0", tk.END), textfeld_correctoutput1.get("1.0", tk.END),
        textfeld_question2.get("1.0", tk.END), textfeld_code2.get("1.0", tk.END), textfeld_correctoutput2.get("1.0", tk.END),
        textfeld_question3.get("1.0", tk.END), textfeld_code3.get("1.0", tk.END), textfeld_correctoutput3.get("1.0", tk.END)
    ))
    submit_button.pack(pady=20)

    submit_button1 = tk.Button(window, text="save as next lvl", command=change_lvl)

    
    submit_button1.pack(pady=20)
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
