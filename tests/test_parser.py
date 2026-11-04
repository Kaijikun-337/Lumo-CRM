import pytest
from app.parsers.factory import ParserFactory
from app.parsers.json_parser import WebhookJSONParser
from app.parsers.csv_parser import CSVParser


def test_webhook_json_parser_dict_input():
    parser = WebhookJSONParser()
    raw_payload = {
        "full_name": "Alice Developer",
        "email_address": "alice@example.com",
        "phone_number": "+1234567890",
        "company": "Tech Corp",
        "budget": "$10k",
    }
    result = parser.parse(raw_payload)

    assert result["name"] == "Alice Developer"
    assert result["email"] == "alice@example.com"
    assert result["phone"] == "+1234567890"
    assert result["custom_fields"] == {"company": "Tech Corp", "budget": "$10k"}


def test_webhook_json_parser_string_input():
    parser = WebhookJSONParser()
    raw_json_str = '{"contact_name": "Bob", "user_email": "bob@example.com", "role": "CTO"}'
    result = parser.parse(raw_json_str)

    assert result["name"] == "Bob"
    assert result["email"] == "bob@example.com"
    assert result["phone"] is None
    assert result["custom_fields"] == {"role": "CTO"}


def test_csv_parser_string_input():
    parser = CSVParser()
    raw_csv_str = "First_Name,Mail,Telephone,Lead_Source\nCharlie,charlie@example.com,555-0199,Google Ads"
    result = parser.parse(raw_csv_str)

    assert result["name"] == "Charlie"
    assert result["email"] == "charlie@example.com"
    assert result["phone"] == "555-0199"
    assert result["custom_fields"] == {"Lead_Source": "Google Ads"}


def test_csv_parser_dict_input():
    parser = CSVParser()
    raw_row = {
        "Name": "Diana",
        "Email": "diana@example.com",
        "Industry": "SaaS",
    }
    result = parser.parse(raw_row)

    assert result["name"] == "Diana"
    assert result["email"] == "diana@example.com"
    assert result["phone"] is None
    assert result["custom_fields"] == {"Industry": "SaaS"}


def test_parser_factory_resolution():
    assert isinstance(ParserFactory.get_parser("webhook"), WebhookJSONParser)
    assert isinstance(ParserFactory.get_parser("json"), WebhookJSONParser)
    assert isinstance(ParserFactory.get_parser("csv"), CSVParser)


def test_parser_factory_unknown_source():
    with pytest.raises(ValueError, match="No parser registered"):
        ParserFactory.get_parser("invalid_type")