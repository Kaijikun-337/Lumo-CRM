import json
from app.parsers.base import BaseParser

class WebhookJSONParser(BaseParser):
    NAME_ALIASES = {"name", "full_name", "contact_name"}
    EMAIL_ALIASES = {"email", "email_address", "user_email"}
    PHONE_ALIASES = {"phone", "phone_number", "mobile", "telephone"}
    
    def parse(self, raw_payload: str | dict) -> dict:
        
        if isinstance(raw_payload, str):
            payload_dict = json.loads(raw_payload)
        else:
            payload_dict = dict(raw_payload)
            
        def extract_first_match(aliases: set[str]) -> str | None:
            for key in list(payload_dict.keys()):
                if key.lower() in aliases:
                    return str(payload_dict.pop(key))
            return None
        
        name = extract_first_match(self.NAME_ALIASES) or "Unknown Lead"
        email = extract_first_match(self.EMAIL_ALIASES)
        phone = extract_first_match(self.PHONE_ALIASES)
        
        custom_fields = payload_dict
        
        return self.normalize_output(
            name=name,
            email=email,
            phone=phone,
            custom_fields=custom_fields
        )