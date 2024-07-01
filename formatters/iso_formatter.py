from datetime import datetime


def iso_format_date(date: datetime) -> str:
    return date.replace(microsecond=0).isoformat() + ".000Z"
