from typing import Any

class Validators:

    @staticmethod
    def required(value: Any) -> tuple[bool, str]:
        print("REQUIRED CHECK")
        if value is None or (isinstance(value, str) and not value.strip()):
            return False, "This field is required."
        return True, ""
    
    @staticmethod
    def is_hex(value: str) -> tuple[bool, str]:
        print(f"IS HEX {value}")
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
        
    @staticmethod
    def valid_ds_year(value: str) -> tuple[bool, str]:
        try:
            int(value)
            if value >= 2000 and value <= 2099:
                return True, ""
            return False, "Number must be between 2000 and 2099."
        except:
            return False, "Value should be a number between 2000 and 2099."
        
    @staticmethod
    def valid_hour(value: str) -> tuple[bool, str]:
        try:
            int(value)
            if value <= 24 and value >= 0:
                return True, ""
            return False, "Value must be between 0 and 24."
        
        except ValueError:
            return False, "Value must be a number bewteen 0 and 24."
        

    def valid_minute_or_second(value: str) -> tuple[bool, str]:
        try:
            int(value)
            if value <= 60 and value >= 0:
                return True, ""
            return False, "Value must be between 0 and 60"
        except ValueError:
            return False, "Value must be a number between 0 and 60"