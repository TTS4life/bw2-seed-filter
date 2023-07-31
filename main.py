#!/usr/bin/python3

import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import drilbur_filter
import tepig_filter

selected_file = None
output_file = None

def browse_file():
    global selected_file
    selected_file = filedialog.askopenfilename()
    file_label.configure(text=get_file_label_text())

def get_file_label_text():
    global selected_file
    if(selected_file is None):
        return "No file selected"

    return selected_file.split("/")[-1]

def prompt_save_file():
    global selected_file, output_file
    if selected_file:
        output_file = filedialog.asksaveasfilename(initialfile='result.txt', defaultextension='.txt')

def find_drilbur():
    global selected_file, output_file
    prompt_save_file()
    drilbur_filter.main(selected_file, output_file)

def find_tepig():
    global selected_file, output_file
    prompt_save_file()
    tepig_filter.main(selected_file, output_file)

root = tk.Tk()

root.title("BW2 Seed Filter")
root.geometry('300x200')

ico = Image.open('kyurem-white.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)

# Configure style
style = ttk.Style(root)
root.config(bg="#26242f")
style.theme_use('clam')
style.configure('TButton', foreground='#FFF', 
                           background='#333', 
                           font=('Helvetica', 12, 'bold'),
                           borderwidth=0)
style.configure('TLabel', foreground='#FFF', background='#26242f', font=('Helvetica', 12, 'bold'))


file_label = ttk.Label(root, text=get_file_label_text())             

browse_button = ttk.Button(root, text="Browse", command=browse_file)
drilbur_button = ttk.Button(root, text="Process Drilburs", command=find_drilbur)
tepig_button = ttk.Button(root, text="Process Tepigs", command=find_tepig)


file_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
browse_button.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
drilbur_button.grid(row=2, column=1, padx=10, pady=10)
tepig_button.grid(row=2, column=2, padx=10, pady=10)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()