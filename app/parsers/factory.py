from app.parsers.base import BaseParser
from app.parsers.csv_parser import CSVParser
from app.parsers.json_parser import WebhookJSONParser

class ParserFactory:
    _paresers: dict[str, type[BaseParser]]={
        "webhook":WebhookJSONParser,
        "json":WebhookJSONParser,
        "csv":CSVParser
    }
    
    @classmethod
    def get_parser(cls, source_type: str) -> BaseParser:
        parser_cls = cls._paresers.get(source_type.lower())
        
        if not parser_cls:
            raise ValueError(f"No parser registered for source_type: '{source_type}'")
        return parser_cls()