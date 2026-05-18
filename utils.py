from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def get_timestamps_with_offset(hours_back_in_time) -> tuple[str, str]:
    now = datetime.now(ZoneInfo("Europe/Berlin")).replace(minute=0, second=0, microsecond=0)
    start_time = now - timedelta(hours=hours_back_in_time)
    end_time = now - timedelta(hours=1)
    start_time_str = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    end_time_str = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    return end_time_str, start_time_str

def get_color(no2_value):
    # Example: Map NO2 to red intensity (0-255)
    intensity = min(int((no2_value / 100) * 255), 255)  # Assume max 100 for scaling
    return [intensity, 0, 255 - intensity, 160]