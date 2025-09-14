#! /usr/bin/env python3

import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
# from PIL import Image, ImageTk
import drilbur_filter
import tepig_filter
import pups
from trainer_skips import TSkipWindow

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

def find_pups():
    global selected_file, output_file
    prompt_save_file()
    pups.main(selected_file, output_file)

def find_tepig_single_seed():
    global tk
    newWindow = tk.Toplevel()
    newWindow.title("Tepig Seed")
    newWindow.config(height="800", width="400")

    style = ttk.Style(newWindow)
    newWindow.config(bg="#26242f")
    style.theme_use('clam')
    style.configure('TButton', foreground='#FFF', 
                            background='#333', 
                            font=('Helvetica', 12, 'bold'),
                            borderwidth=0)
    style.configure('TLabel', foreground='#FFF', background='#26242f', font=('Helvetica', 12, 'bold'))

    seed = tk.StringVar()
    ivframe = tk.StringVar()
    month = tk.StringVar()

    # ttk.Label(newWindow, text=f"{seed.seed}")
    ttk.Label(newWindow, text="Tepig Seed: ", justify="left").grid(row=0, column=0)
    ttk.Label(newWindow, text="IV Frame: ", justify="left").grid(row=1, column=0)

    seed_entry = ttk.Entry(newWindow, textvariable=seed, justify='left')
    seed_entry.grid(row=0, column=1)
    
    ivframe_entry = ttk.Entry(newWindow, textvariable=ivframe, justify="left")
    ivframe_entry.grid(row=1, column=1)

    ttk.Label(newWindow, text="month").grid(row=2, column=0)
    month_entry = ttk.Entry(newWindow, textvariable=month, justify="center" )
    month_entry.grid(row=2, column=1)

    results_text = tk.Text(newWindow)
    results_text.grid(row=6, column=1)

    ttk.Button(newWindow, text="Run", command=lambda: process_tepig_seed_button_click(seed_entry.get(), ivframe_entry.get(), month_entry.get(), results_text)).grid(row=4, column=1, columnspan=3)
    
    newWindow.focus()
    newWindow.mainloop()
    # seed = tepig_filter.processSeed()

def trainerSkips():
    global tk
    newWindow = tk.Toplevel()
    TSkipWindow.createTSkipWindow(newWindow)


def process_tepig_seed_button_click(seed, ivframe, month, results_text):
    
    if(results_text.compare("end-1c", "!=", "1.0")):
        results_text.delete("1.0", "end")

    try:
        print("Processing Seed...")
        seed = tepig_filter.processSeed(seed, ivframe, month)
    except Exception as ex:
        results_text.insert(tk.INSERT, "Exception occurred: " + str(ex))
        return
    if(seed is None):
        results_text.insert(tk.INSERT, "Issue getting data.")
        return
    if(results_text is None):
        print("Error getting label to print seed out to")
        return 
    
    results_text.insert(tk.INSERT, seed)
    print("Done")
    return

root = tk.Tk()

root.title("BW/BW2 Seed Filter")
root.geometry('500x400')

# ico = Image.open('kyurem-white.png')
# photo = ImageTk.PhotoImage(ico)
# root.wm_iconphoto(False, photo)

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
drilbur_button = ttk.Button(root, text="Drilbur Filter", command=find_drilbur)
tepig_button = ttk.Button(root, text="Tepig Filter", command=find_tepig)
tepig_seed_button = ttk.Button(root, text="View Tepig Seed", command=find_tepig_single_seed)
pup_seed_button = ttk.Button(root, text="Lillipup Filter", command=find_pups)
trainer_skip_button = ttk.Button(root, text="Trainer Skip Generator", command=trainerSkips)


step1 = ttk.Label(text="Step 1: Choose File to load: ")
step1.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

file_label.grid(row=1, column=1, columnspan=3, padx=10, pady=10)
browse_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

step2 = ttk.Label(text="Step 2: Filter File as: ")
step2.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

drilbur_button.grid(row=4, column=1, padx=10, pady=10)
tepig_button.grid(row=4, column=2, padx=10, pady=10)
tepig_seed_button.grid(row=5, column=2, padx=10, pady=10)
pup_seed_button.grid(row=5, column=1, padx=10, pady=10)

misc_tools = ttk.Label(text="Miscellaneous tools/Generators")
misc_tools.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

trainer_skip_button.grid(row=7, column=1, padx=10, pady=10)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()