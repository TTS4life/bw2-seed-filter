import tkinter as tk
from tkinter import ttk
from FieldData import FieldDefinition, DataWorker
from types import List, Dict, Optional, Any
from GenericForm import GenericForm

class FormController:
    def __init__(self, root):
        self.root = root
        self.forms = []
        self.current_form = None

    def create_form(self, title: str, fields: List[FieldDefinition], worker: Optional[DataWorker] = None) -> GenericForm:
        form = GenericForm(self.root, title, fields, worker)
        form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.forms.append(form)
        self.current_form = form
        return form
    

    def set_active_worker(self, worker: DataWorker):
        if self.current_form:
            self.current_form.set_worker(worker)