from .GenericForm import GenericForm
from .FieldData import FieldDefinition
from numba_pokemon_prngs.enums import Game, Language, DSType
from .FormController import FormController
from tkinter import ttk
import tkinter as tk

GAME_MAPPING = {
    "Black": Game.BLACK,
    "White": Game.WHITE,
    "Black 2": Game.BLACK2,
    "White 2": Game.WHITE2
}


class Gen5GeneratorForm(GenericForm):

    def __init__(self, window):

        style = ttk.Style(window)



        fields = [
            FieldDefinition(
                name="version",
                label="Version",
                field_type="dropdown",
                required=True,
                options=["Black", "White", "Black 2", "White 2"],
                default="White 2"
            ),
            FieldDefinition(
                name="language",
                label="Language",
                field_type="dropdown",
                options=["English", "Japanese"],
                default="English",
                required=True
            )
        ]
        controller = FormController(window)
        
        window.config(bg="#26242f")
        style.theme_use('clam')
        style.configure('TButton', foreground='#FFF', 
                                background='#333', 
                                font=('Helvetica', 12, 'bold'),
                                borderwidth=0,)
        style.configure('TLabel', foreground='#FFF', background='#26242f', font=('Helvetica', 12, 'bold'))
        style.configure('TCheckbutton', foreground='#FFF', background='#26242f', font=('Helvetica', 12, 'bold'), indicatormargin=4, highlightthickness=0, borderwidth=0)

        style.map("TCheckbutton",
            background=[('active', '#26242f')],
            foreground=[('active', '#FFF')])
        form = controller.create_form("Generic Test", fields)




        