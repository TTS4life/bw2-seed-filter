import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from .FieldData import FieldDefinition, DataWorker, FormData

from typing import List, Optional, Dict, Any

class GenericForm(ttk.Frame):

    def __init__(self, parent, title: str, fields: List[FieldDefinition], worker: Optional[DataWorker] = None, **kwargs ):
        super().__init__(parent, **kwargs)
        self.title = title
        self.fields_def = fields
        self.worker = worker
        self.field_widgets = {}
        self.error_labels = {}
        self.result_callabck = None

        self._create_widgets()
        self._layout_widgets()

    def apply_styles(self):
        """Apply consistent styles to form widgets"""
        # Style the form frame itself
        self.configure(style='Main.TFrame')
        
        # Style title
        if hasattr(self, 'title_label'):
            self.title_label.configure(style='Heading.TLabel')
        
        # Style all field labels
        for child in self.winfo_children():
            if isinstance(child, ttk.Label) and child != self.title_label:
                child.configure(style='Main.TLabel')
        
        # Style entry widgets
        for field_def in self.fields_def:
            widget = self.field_widgets.get(field_def.name)
            if widget:
                if field_def.field_type == 'text' and isinstance(widget, ttk.Entry):
                    widget.configure(style='Form.TEntry')
                elif field_def.field_type == 'dropdown' and isinstance(widget, ttk.Combobox):
                    widget.configure(style='Form.TCombobox')
        
        # Style buttons
        if hasattr(self, 'submit_btn'):
            self.submit_btn.configure(style='Primary.TButton')
        if hasattr(self, 'cancel_btn'):
            self.cancel_btn.configure(style='Secondary.TButton')
        
        # Style error labels
        for error_label in self.error_labels.values():
            error_label.configure(style='Error.TLabel')


        def create_styled_message(self, message: str, message_type: str = 'error'):
            """Create a styled message label"""
            style = 'Error.TLabel' if message_type == 'error' else 'Success.TLabel'
        
            if hasattr(self, 'message_label'):
                self.message_label.configure(text=message, style=style)
            else:
                self.message_label = ttk.Label(self, text=message, style=style)
                self.message_label.grid(row=100, column=0, columnspan=3, pady=10)

    def _create_widgets(self):
        self.title_label = ttk.Label(self, text=self.title, font=('Arial', 14, 'bold'))

        for field_def in self.fields_def:
            label = ttk.Label(self, text=field_def.label + (f" *") if field_def.required else "")

            if field_def.field_type == 'text':
                widget = ttk.Entry(self, width=field_def.width)
                if field_def.default:
                    widget.insert(0, field_def.default)
            
            elif field_def.field_type == 'dropdown':
                widget = ttk.Combobox(self, values=field_def.options or [], width=field_def.width, state='readonly')

                if field_def.default:
                    widget.set(field_def.default)
                elif field_def.options:
                    widget.current(0)

            elif field_def.field_type == 'checkbox':
                var = tk.BooleanVar(value=field_def.default or False)
                widget = ttk.Checkbutton(self,variable=var)
                self.field_widgests[field_def.name] = var

            else:
                raise ValueError(f"Unknown field type {field_def.field_type} for component {field_def.name}")
            

            error_label = ttk.Label(self, text="", foreground="red", font=('Arial', 9))

            self.field_widgets[field_def.name] = widget
            self.error_labels[field_def.name] = error_label

        if hasattr(self, 'worker_selector'):
            self.worker_selector = None


    def _layout_widgets(self):
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")

        row = 1
        for field_def in self.fields_def:
            label_text = field_def.label + (" *" if field_def.required else "")
            ttk.Label(self, text=label_text).grid(
                row=row, column=0, sticky="w", padx=(0, 10), pady=5
            )

            if field_def.field_type == 'checkbox':
                self.field_widgets[field_def.name].grid(
                    row=row, column=1, sticky="w", pady=5
                )
            else:
                self.field_widgets[field_def.name].grid(
                    row=row, column=1, sticky="ew", padx=(0, 10), pady=5
                )

            self.error_labels[field_def.name].grid(
                row=row, column=2, sticky="w", pady=5
            )

            row += 1

        button_frame = ttk.Frame(self)
        button_frame.grid(row=row, column=0, columnspan=3, pady=(20, 0))

        self.run_btn = ttk.Button(button_frame, text="Run", command=self._on_submit, style="Primary.TButton")

        self.run_btn.pack(side=tk.LEFT, padx=5)

        self.grid_columnconfigure(1, weight=1)

    
    def _on_submit(self):
        form_data = self.get_data()

        if form_data.is_valid:
            self._clear_errors()

            #Prompt and add save location to fields for the worker
            form_data.fields.update(output_file=filedialog.asksaveasfilename())

            #Worker stuff here
            self.worker.process(form_data)

    
    def _validate_field(self, field_def: FieldDefinition, value: Any) -> tuple[bool, str]:
        # print(f"VALIDATING {field_def.name} value {value}")
        if field_def.required:
            if value is None or (isinstance(value, str) and not value.strip()):
                return False, f"{field_def.label} is required"
            
        if field_def.validator and value:
            return field_def.validator(value)
        
        return True, ""
    

    def get_data(self) -> FormData:
        form_data = FormData()
        is_valid = True

        for field_def in self.fields_def:
            widget = self.field_widgets[field_def.name]

            if field_def.field_type == 'checkbox':
                value = widget.get()
            elif field_def.field_type in ['text', 'dropdown']:
                value = widget.get().strip()
            else:
                value = widget.get()

            valid, error_msg = self._validate_field(field_def, value)

            if not valid:
                is_valid = False
                form_data.errors[field_def.name] = error_msg

            form_data.fields[field_def.name] = value

        form_data.is_valid = is_valid

        print(f"Form Valid? {is_valid}")
        return form_data
    
    def _display_errors(self, errors: Dict[str, str]):
        for field_name, error in errors.items():
            if field_name in self.error_labels:
                self.error_labels[field_name].config(text=error)

    def _clear_errors(self):
        for error_label in self.error_labels.values():
            error_label.config(text="")

    def _show_messasge(self, message: str, color: str = "white"):
        if hasattr(self, 'message_label'):
            self.message_label.config(text=message, foreground=color)

    def clear_form(self):
        """Clear all form fields"""
        for field_def in self.fields_def:
            widget = self.field_widgets[field_def.name]
            
            if field_def.field_type == 'text':
                widget.delete(0, tk.END)
                if field_def.default:
                    widget.insert(0, field_def.default)
            elif field_def.field_type == 'dropdown':
                if field_def.default:
                    widget.set(field_def.default)
                elif field_def.options:
                    widget.current(0)
            elif field_def.field_type == 'checkbox':
                widget.set(field_def.default or False)
        
        self._clear_errors()
        if hasattr(self, 'message_label'):
            self.message_label.config(text="")