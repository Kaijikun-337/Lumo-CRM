import csv
import io
from app.parsers.base import BaseParser


class CSVParser(BaseParser):
    NAME_ALIASES = {"name", "full_name", "contact_name", "first_name"}
    EMAIL_ALIASES = {"email", "email_address", "mail", "user_email"}
    PHONE_ALIASES = {"phone", "phone_number", "mobile", "telephone"}

    def parse(self, raw_payload: str | dict) -> dict:
        if isinstance(raw_payload, str):
            f = io.StringIO(raw_payload.strip())
            reader = csv.DictReader(f)
            payload_dict = next(reader, {})
        else:
            payload_dict = dict(raw_payload)

        def extract_first_match(aliases: set[str]) -> str | None:
            for key in list(payload_dict.keys()):
                if key and key.strip().lower() in aliases:
                    val = payload_dict.pop(key)
                    return str(val).strip() if val else None
            return None

        name = extract_first_match(self.NAME_ALIASES) or "Unknown Lead"
        email = extract_first_match(self.EMAIL_ALIASES)
        phone = extract_first_match(self.PHONE_ALIASES)

        custom_fields = {k.strip(): v for k, v in payload_dict.items() if k}

        return self.normalize_output(
            name=name,
            email=email,
            phone=phone,
            custom_fields=custom_fields
        )