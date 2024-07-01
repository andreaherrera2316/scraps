from datetime import datetime


def ymd_format_date(date: datetime) -> str:
    return date.strftime("%Y-%m-%d")
