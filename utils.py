from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def get_timestamps_with_offset() -> tuple[str, str]:
    now = datetime.now(ZoneInfo("Europe/Berlin")).replace(minute=0, second=0, microsecond=0)
    start_time = now - timedelta(hours=240)
    end_time = now - timedelta(hours=216)
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    return end_time_str, start_time_str