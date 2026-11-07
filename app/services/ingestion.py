import json
from app.database import SessionLocal
from app.models import RawIngestionLog, Lead, Source
from app.parsers.factory import ParserFactory


def process_raw_ingestion_log(log_id: int):
    """Background task to parse stored raw ingestion logs and create normalized Leads."""
    db = SessionLocal()
    try:
        log = db.query(RawIngestionLog).filter(RawIngestionLog.id == log_id).first()
        if not log:
            return

        source = db.query(Source).filter(Source.id == log.source_id).first()
        if not source:
            log.status = "FAILED"
            log.error_message = f"Associated Source ID {log.source_id} missing."
            db.commit()
            return

        # Decode JSON string or raw text payload from log entry
        try:
            payload_data = json.loads(log.payload)
        except Exception:
            payload_data = log.payload

        # Run strategy parser
        parser = ParserFactory.get_parser(source.source_type)
        normalized = parser.parse(payload_data)

        # Create Lead record
        db_lead = Lead(
            name=normalized["name"],
            email=normalized.get("email"),
            phone=normalized.get("phone"),
            custom_fields=normalized.get("custom_fields", {}),
            project_id=source.project_id,
            source_id=source.id,
        )
        db.add(db_lead)

        # Update audit log status
        log.status = "SUCCESS"
        db.commit()

    except Exception as e:
        db.rollback()
        # Re-query log within aborted transaction state to log failure
        log = db.query(RawIngestionLog).filter(RawIngestionLog.id == log_id).first()
        if log:
            log.status = "FAILED"
            log.error_message = str(e)
            db.commit()
    finally:
        db.close()