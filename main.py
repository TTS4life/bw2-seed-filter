#! /usr/bin/env python3

import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
# from PIL import Image, ImageTk
import drilbur_filter
import tepig_filter
import pups
from trainer_skips import TSkipWindow

from ui.Gen5GeneratorForm import Gen5GeneratorForm
from ui.FormController import FormController
from ui.GenericForm import GenericForm
from ui.styles import configure_app_styles


def create_button_grid(parent, buttons_data, columns=2, start_row=0, uniform_weight=True, **grid_kwargs):
    buttons = []

    if 'sticky' not in grid_kwargs:
        grid_kwargs['sticky'] = 'ew'

    for col in range(0, columns):
        parent.grid_columnconfigure(col, weight=1, uniform='button_cols' if uniform_weight else None)

    for i, button_config in enumerate(buttons_data):
        row = start_row + (i // columns)
        col = i % columns

        button = ttk.Button(parent, **button_config, style='Primary.TButton')

        button.grid(row=row, column=col, padx=10, pady=5, **grid_kwargs)
        buttons.append(button)

    total_rows = (len(buttons_data) + columns - 1) // columns
    # for row in range(start_row, start_row + total_rows):
        # parent.grid_rowconfigure(row, weight=1)
    for col in range(columns):
        parent.grid_rowconfigure(col, weight=1)

    return buttons


def main():
    root = tk.Tk()

    root.title("BW/BW2 Seed Filter")
    root.geometry('500x400')

    # ico = Image.open('kyurem-white.png')
    # photo = ImageTk.PhotoImage(ico)
    # root.wm_iconphoto(False, photo)

    # Configure style
    style, colors, fonts = configure_app_styles()

    root.configure(bg=colors['bg'])

    selected_file = tk.StringVar()
    full_path = None

    def browse_file():
        global full_path
        filename = filedialog.askopenfilename(title="Select a file to parse.")
        if filename:
            selected_file.set(filename.split("/")[-1])
            full_path = filename

    def prompt_save_file():
        global output_file
        if selected_file:
            return filedialog.asksaveasfilename(initialfile='result.txt', defaultextension='.txt')

    def find_drilbur():
        global full_path
        output_file = prompt_save_file()
        drilbur_filter.main(full_path, output_file)

    def find_tepig():
        global full_path
        output_file = prompt_save_file()
        print(f"{full_path}, {output_file}")
        tepig_filter.main(full_path, output_file)

    def find_pups():
        global full_path
        output_file = prompt_save_file()
        pups.main(selected_file, output_file)

    def find_tepig_single_seed():
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
        Gen5GeneratorForm(newWindow)

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
        

    selected_file.set("No file Selected.")
    file_label = ttk.Label(root, textvariable=selected_file, style="Main.TLabel")             

    browse_button = ttk.Button(root, text="Browse", command=browse_file, style="Primary.TButton")



    filter_buttons = [
        {"text": "Drilbur Filter", "command": find_drilbur},
        {"text": "Tepig Filter", "command": find_tepig},
        {"text": "Lilliipup Filter", "command": find_pups},
        {"text": "View Tepig Seed", "command": find_tepig_single_seed},
    ]


    
    step1 = ttk.Label(text="Step 1: Choose File to load: ", style="Main.TLabel")
    step1.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

    file_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
    browse_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=1)


    step2 = ttk.Label(text="Step 2: Filter File as: ", style='Main.TLabel')
    step2.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    buttons = create_button_grid(root, filter_buttons, columns = 2, start_row=4, sticky='ew')

    misc_tools = ttk.Label(text="Miscellaneous tools/Generators", style='Main.TLabel')
    misc_tools.grid(row=6, column=0, columnspan=3, padx=10, pady=10)

    trainer_skip_button = ttk.Button(root, text="Trainer Skip Generator", command=trainerSkips, style="Primary.TButton")
    trainer_skip_button.grid(row=7, column=1, padx=10, pady=10)


    root.mainloop()


if __name__ == '__main__':
    main()