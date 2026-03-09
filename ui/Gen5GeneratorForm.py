from .GenericForm import GenericForm
from .FieldData import FieldDefinition
from .FormController import FormController
from tkinter import ttk
import tkinter as tk
from .FormValidators import Validators
from trainer_skips.TrainerSkipWorker import TrainerSkipWorkerHandler


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
            ),
            FieldDefinition(
                name="timer0",
                label="Timer0",
                field_type="text",
                required=True,
                validator=Validators.is_hex
            ),
            FieldDefinition(
                name="month",
                label="Month",
                field_type="dropdown",
                options=[1,2,3,4,5,6,7,8,9,10,11,12],
                default=1,
                required=True,
            ),
            FieldDefinition(
                name="day",
                label="Day",
                field_type="dropdown",
                options=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
                required=True
            ),
            FieldDefinition(
                name="year",
                label="Year",
                field_type="text",
                default="2000",
                required=True,
                validator=Validators.valid_ds_year,
            ),
            FieldDefinition(
                name="mac",
                label="Mac Address",
                field_type="text",
                validator=Validators.is_hex,
                required=True
            ),
            FieldDefinition(
                name="hour",
                label="Hour",
                field_type="text",
                validator=Validators.valid_hour,
                required=True
            ),
            FieldDefinition(
                name="minute",
                label="Minute",
                field_type="text",
                required=True,
                validator=Validators.valid_minute_or_second
            )
        ]
        controller = FormController(window)

        form = controller.create_form("Trainer Skips", fields, TrainerSkipWorkerHandler())




        