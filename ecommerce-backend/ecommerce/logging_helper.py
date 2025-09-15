import logging

logger = logging.getLogger("ecommerce")

def log_event(event_name, payload=None, level="INFO"):
    """
    Logs an event in JSON format with request_id, event name, payload, timestamp.
    """
    extra = {
        "event": event_name,
        "payload": payload if payload else {},
    }

    if level.upper() == "INFO":
        logger.info(event_name, extra=extra)
    elif level.upper() == "ERROR":
        logger.error(event_name, extra=extra, exc_info=True)
