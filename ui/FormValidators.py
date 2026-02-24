from typing import Any

class Validators:

    @staticmethod
    def required(value: Any) -> tuple[bool, str]:
        if value is None or (isinstance(value, str) and not value.strip()):
            return False, "This field is required."
        return True, ""
    
    @staticmethod
    def hex(value: str) -> tuple[bool, str]:
        if not value:
            return True, "" #Empty no bueno
        try:
            int(value, 16)
            return True, ""
        except ValueError:
            return False, "Entered value is not hexidecimal"
        
    @staticmethod
    def is_number(value: str) -> tuple[bool, str]:
        try:
            int(value)
            return True, ""
        except ValueError:
            return False, "Value must be a number."