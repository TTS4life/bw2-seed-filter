import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
from datetime import datetime
from numba_pokemon_prngs.enums import Language, Game, DSType
from trainer_skips import w2_thewholeskip, thewholeskip
from trainer_skips.Parameters import parameters
from trainer_skips.sharedfuncs import compute_times_tospring

game_version_cb = None
game_language = None
mac_addr = None
eYear = None
mCombo = None 
domCombo = None 
eTimer0 = None
eHour = None
eMinute = None
errText = None
Twindow = None
parameters_instance = None
compute_time_spring_var = None  # チェックボックス用の変数

def on_time_spring_checkbox_change():
    """Time Springチェックボックスの状態変更時のコールバック"""
    global eHour, eMinute, compute_time_spring_var
    
    if compute_time_spring_var.get():
        # チェックボックスがオンになった場合、hourとminuteを無効化
        eHour.config(state='disabled')
        eMinute.config(state='disabled')
        # Time Springの時間を表示
        spring_times = compute_times_tospring()
        if spring_times:
            # 最初の時間を表示
            hour, minute, second = spring_times[0]
            eHour.config(state='normal')
            eHour.delete(0, tk.END)
            eHour.insert(0, str(hour))
            eHour.config(state='disabled')
            
            eMinute.config(state='normal')
            eMinute.delete(0, tk.END)
            eMinute.insert(0, str(minute))
            eMinute.config(state='disabled')
    else:
        # チェックボックスがオフになった場合、hourとminuteを有効化
        eHour.config(state='normal')
        eMinute.config(state='normal')

def createTSkipWindow(window):
    global game_version_cb, game_language, mac_addr, eYear, mCombo, domCombo, eTimer0, eHour, eMinute, errText, Twindow, parameters_instance, compute_time_spring_var

    Twindow = window
    parameters_instance = parameters()  # インスタンスを作成

    window.title("Trainer Skips")
    window.geometry("500x550")
    style = ttk.Style(window)
    window.config(bg="#26242f")
    style.theme_use('clam')
    style.configure('TButton', foreground='#FFF', 
                            background='#333', 
                            font=('Helvetica', 12, 'bold'),
                            borderwidth=0)
    style.configure('TLabel', foreground='#FFF', background='#26242f', font=('Helvetica', 12, 'bold'))
    style.configure('TCheckbutton', foreground='#FFF', background='#26242f', font=('Helvetica', 12, 'bold'))


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
    
    #Timer0
    ttk.Label(window, text="Timer0").grid(row=6, column=0, padx=10, pady=10)
    eTimer0 = ttk.Entry(window)
    eTimer0.grid(row=6, column=1, padx=10, pady=10)
    
    #Hour
    ttk.Label(window, text="Hour").grid(row=7, column=0, padx=10, pady=10)
    eHour = ttk.Entry(window)
    eHour.grid(row=7, column=1, padx=10, pady=10)
    eHour.insert(0, "12")  # デフォルト値を設定
    
    #Minute
    ttk.Label(window, text="Minute").grid(row=8, column=0, padx=10, pady=10)
    eMinute = ttk.Entry(window)
    eMinute.grid(row=8, column=1, padx=10, pady=10)
    eMinute.insert(0, "0")  # デフォルト値を設定

    # Time Spring チェックボックス（Hour/Minuteの横に配置）
    compute_time_spring_var = tk.BooleanVar()
    compute_time_spring_cb = ttk.Checkbutton(window, text="Time Spring", variable=compute_time_spring_var, command=on_time_spring_checkbox_change)
    compute_time_spring_cb.grid(row=7, column=2, rowspan=2, padx=10, pady=10, sticky="w")

    errText = tk.StringVar()
    errLabel = ttk.Label(window, textvariable=errText)
    errLabel.grid(row=9, column=1, padx=10, pady=10)
    errText.set("")

    runButton = ttk.Button(window, text="Run", command=run)
    runButton.grid(row=10, column=1)

    window.mainloop()

def calculate_day_of_week(year, month, day):
    """年、月、日から曜日を計算する"""
    try:
        date_obj = datetime(year, month, day)
        # datetime.weekday()は月曜日=0, 日曜日=6を返す
        # ゲームの仕様に合わせて調整（日曜日=0, 月曜日=1, ...）
        weekday = date_obj.weekday()
        return (weekday + 1) % 7  # 日曜日を0にする
    except ValueError:
        raise ValueError(f"無効な日付です: {year}/{month}/{day}")

# ゲームバージョンのマッピング辞書
GAME_MAPPING = {
    "Black": Game.BLACK,
    "White": Game.WHITE,
    "Black 2": Game.BLACK2,
    "White 2": Game.WHITE2
}

# 言語のマッピング辞書
LANGUAGE_MAPPING = {
    "English": Language.ENGLISH,
    "Japanese": Language.JAPANESE
}

def mapGame(params, combo):
    game_name = combo.get()
    if game_name in GAME_MAPPING:
        params.Version = GAME_MAPPING[game_name]
    else:
        raise ValueError(f"Unknown game version: {game_name}")

def mapLanguage(params, combo):
    language_name = combo.get()
    if language_name in LANGUAGE_MAPPING:
        params.Language = LANGUAGE_MAPPING[language_name]
    else:
        raise ValueError(f"Unknown language: {language_name}")

def run():
    global errText, Twindow, eYear, mCombo, domCombo, mac_addr, eTimer0, eHour, eMinute, game_version_cb, game_language, parameters_instance, compute_time_spring_var

    try:
        # バージョンによって保存ダイアログと拡張子を分岐
        game_name = game_version_cb.get() if game_version_cb else None
        if game_name in ('Black', 'White'):
            outfile = filedialog.asksaveasfilename(initialfile="trainerskip.txt", defaultextension=".txt")
        else:
            outfile = filedialog.asksaveasfilename(initialfile="trainerskip.xlsx", defaultextension=".xlsx")
    except:
        return

    if(not eYear.get().isnumeric() or not mCombo.get().isnumeric() or not domCombo.get().isnumeric()
      or not eHour.get().isnumeric() or not eMinute.get().isnumeric()
      # or not eTimer0.get().isnumeric() #or not mac_addr.get().isnumeric()
       ):
        print('bad input')
        errText.set("Bad Input.")
        return

    try:
        # 年、月、日を取得
        year = int(eYear.get())
        month = int(mCombo.get())
        day = int(domCombo.get())
        
        # 時間を取得
        hour = int(eHour.get())
        minute = int(eMinute.get())
        
        # 時間の範囲をチェック
        if hour < 0 or hour > 23:
            errText.set("Hour must be between 0 and 23")
            return
        if minute < 0 or minute > 59:
            errText.set("Minute must be between 0 and 59")
            return
        
        # Time Springの計算が有効な場合
        if compute_time_spring_var.get():
            try:
                # sharedfuncsのcompute_times_tospring関数を使用
                spring_times = compute_times_tospring()
                # print(f"Time Spring times: {spring_times}")
                # Time Springが有効な場合は、ユーザーの入力に関係なくTime Springの時間を使用
                if spring_times:
                    # 最初の時間を使用（または他の選択ロジック）
                    hour, minute, second = spring_times[0]
                    print(f"Using Time Spring time: {hour}:{minute}:{second}")
                else:
                    errText.set("No Time Spring times available")
                    return
            except Exception as e:
                errText.set(f"Time Spring calculation error: {e}")
                return
        
        # 曜日を自動計算
        parameters_instance.DOW = calculate_day_of_week(year, month, day)

        #Version
        mapGame(parameters_instance, game_version_cb)

        #Language
        mapLanguage(parameters_instance, game_language)
        
        # ゲーム設定に応じてパラメータを設定
        game_name = game_version_cb.get()
        language_name = game_language.get()
        
        if game_name in ('Black', 'White'):
            if language_name == 'English':
                parameters_instance.setENGB1()
            else:  # Japanese
                if game_name == 'Black':
                    parameters_instance.setJPNB1()
                else:  # White
                    parameters_instance.setJPNW1()
        else:  # Black 2, White 2
            if language_name == 'English':
                parameters_instance.setENGW2()
            else:  # Japanese
                parameters_instance.setJPNW2()
        
    except ValueError as e:
        errText.set(f"Error: {e}")
        return
    
    errText.set("Searching...")

    Twindow.update()

    parameters_instance.Year = year
    parameters_instance.Month = month
    parameters_instance.Day = day
    parameters_instance.Hour = hour
    parameters_instance.Minute = minute
    parameters_instance.MAC = int(mac_addr.get(), 16)
    parameters_instance.Timer0Min = int(eTimer0.get(), 16)
    
    # Time Springフラグを設定
    parameters_instance.use_time_spring = compute_time_spring_var.get()

    if game_version_cb.get() in ('Black', 'White'):
        print("BW1")
        thewholeskip.main(
            parameters_instance,
            outfile
        )
    else:
        print(f"BW2? {game_version_cb}")
        w2_thewholeskip.main(
            parameters_instance,
            outfile
        )

    errText.set("Done!")

    


