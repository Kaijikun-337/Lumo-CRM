from abc import ABC, abstractmethod

class BaseParser(ABC):
    
    @abstractmethod
    def parse(self, raw_payload: str | dict) -> dict:
        pass
    
    def normalize_output(
        self, 
        name: str, 
        email: str | None = None, 
        phone: str | None = None, 
        custom_fields: dict | None = None
    ) -> dict:
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "custom_fields": custom_fields if custom_fields is not None else {}
        }
