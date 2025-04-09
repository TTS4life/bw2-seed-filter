import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
from numba_pokemon_prngs.enums import Language, Game, DSType
from trainer_skips import w2_thewholeskip, thewholeskip
from trainer_skips.Parameters import parameters

game_version_cb = None
game_language = None
mac_addr = None
eYear = None
mCombo = None 
domCombo = None 
dowCombo= None
eTimer0 = None
errText = None
Twindow = None

parameters = parameters()

def createTSkipWindow(window):
    global game_version_cb, game_language, mac_addr, eYear, mCombo, domCombo, dowCombo, eTimer0, errText, Twindow

    Twindow = window

    window.title("Trainer Skips")
    window.geometry("500x450")

    style = ttk.Style(window)
    window.config(bg="#26242f")
    style.theme_use('clam')
    style.configure('TButton', foreground='#FFF', 
                            background='#333', 
                            font=('Helvetica', 12, 'bold'),
                            borderwidth=0)
    style.configure('TLabel', foreground='#FFF', background='#26242f', font=('Helvetica', 12, 'bold'))


    #Game version 
    ttk.Label(window, text="Version").grid(row=0, column=0)

    game_version_cb = ttk.Combobox(window, width=27, state="readonly")
    game_version_cb['values'] = ( 'Black', 'White', 'Black 2', 'White 2')
    game_version_cb.grid(row=0, column=1, padx=10, pady=10)
    game_version_cb.current(0)

    #Game lang
    ttk.Label(window, text="Language").grid(row=1, column=0)

    game_language = ttk.Combobox(window, width=27, state="readonly")
    game_language['values'] = ( 'English', 'Japanese')
    game_language.grid(row=1, column=1, padx=10, pady=10)
    game_language.current(0)

    #MAC Address
    ttk.Label(window, text="MAC Address").grid(row=2, column=0, padx=10, pady=10)
    mac_addr = ttk.Entry(window)
    mac_addr.grid(row=2, column=1, padx=10, pady=10)

    #Year
    ttk.Label(window, text="Year").grid(row=3, column=0, padx=10, pady=10)
    eYear = ttk.Entry(window)
    eYear.grid(row=3, column=1, padx=10, pady=10)
    
    #Month
    ttk.Label(window, text="Month").grid(row=4, column=0, padx=10, pady=10)
    mCombo = ttk.Combobox(window, width=27, state="readonly")
    mCombo.grid(row=4, column=1, padx=10, pady=10)
    mCombo['values'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
    mCombo.current(0)


    #Day
    ttk.Label(window, text="Day of Month").grid(row=5, column=0, padx=10, pady=10)
    domCombo = ttk.Combobox(window, width=27)
    domCombo.grid(row=5, column=1, padx=10, pady=10)
    domCombo['values'] = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', 
                          '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31')
    domCombo.current(0)


    #Day of Week
    ttk.Label(window, text="Day of Week").grid(row=6, column=0, padx=10, pady=10)
    dowCombo = ttk.Combobox(window, width=27, state="readonly")
    dowCombo.grid(row=6, column=1, padx=10, pady=10)
    dowCombo['values'] = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
    dowCombo.current(0)
    
    #Timer0
    ttk.Label(window, text="Timer0").grid(row=7, column=0, padx=10, pady=10)
    eTimer0 = ttk.Entry(window)
    eTimer0.grid(row=7, column=1, padx=10, pady=10)
    

    errText = tk.StringVar()
    errLabel = ttk.Label(window, textvariable=errText)
    errLabel.grid(row=8, column=1, padx=10, pady=10)
    errText.set("")

    runButton = ttk.Button(window, text="Run", command=run)
    runButton.grid(row=9, column=1)

    window.mainloop()

def mapDOW(params, combo):
    match combo.get():
        case "Monday":
            params.DOW = 1
        case "Tuesday":
            params.DOW = 2
        case "Wednesday":
            params.DOW = 3
        case "Thursday":
            params.DOW = 4
        case "Friday":
            params.DOW = 5
        case "Saturday":
            params.DOW = 6
        case "Sunday":
            params.DOW = 0

def mapGame(params, combo):
    match combo.get():
        case "Black":
            params.Version = Game.BLACK
        case "White":
            params.Version = Game.WHITE
        case "Black 2":
            params.Version = Game.BLACK2
        case "White 2":
            params.Version = Game.WHITE2

def mapLanguage(params, combo):
    match combo.get():
        case "English":
            params.Language = Language.ENGLISH
        case "Japanese":
            params.Language = Language.JAPANESE

def run():
    global errText, Twindow


    try:
        outfile = filedialog.asksaveasfilename(initialfile="trainerskip.txt", defaultextension=".txt")
    except:
        return


    if(not eYear.get().isnumeric() or not mCombo.get().isnumeric() or not domCombo.get().isnumeric()
      # or not eTimer0.get().isnumeric() #or not mac_addr.get().isnumeric()
       ):
        print('bad input')
        errText.set("Bad Input.")
        return


    #DOW
    mapDOW(parameters, dowCombo)

    #Version
    mapGame(parameters, game_version_cb)

    #Language
    mapLanguage(parameters, game_language)
    
    
    errText.set("Searching...")

    Twindow.update()

    parameters.Year = int(eYear.get())
    parameters.Month = int(mCombo.get())
    parameters.Day = int(domCombo.get())
    parameters.MAC = int(mac_addr.get(), 16)
    parameters.Timer0Min = int(eTimer0.get(), 16)

    if game_version_cb in ('Black', 'White'):
        thewholeskip.main(
            parameters,
            outfile
        )
    else:
        w2_thewholeskip.main(
            parameters,
            outfile
        )

    errText.set("Done!")

    


