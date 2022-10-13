from tkinter import * 
from tkinter import messagebox

def click():
    messagebox.showinfo(title='This is an info message box', message='You are a person')

def message():
    window=Tk()

    button=Button(window, command=click, text='click me')
    button.pack()