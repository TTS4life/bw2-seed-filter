from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
import re

@dataclass
class FieldDefinition:
    name: str
    label:str
    field_type: str # 'text', 'dropdown', or 'checkbox'
    required: bool = False
    default: Any = None
    options: List[str] = None #Dropdowns only
    validator: Optional[Callable[[Any], tuple[bool, str]]] = None
    width: int = 30

@dataclass
class FormData:
    fields: Dict[str, Any] = field(default_factory=dict)
    errors: Dict[str, str] = field(default_factory=dict)
    is_valid: bool = False

class DataWorker(ABC):

    @abstractmethod
    def process(self, data: FormData) -> Any:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


    