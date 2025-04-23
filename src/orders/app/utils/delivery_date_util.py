from datetime import datetime, timedelta

def get_delivery_date(start_date, days=2):
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    count = 0
    while count < days:
        start_date += timedelta(days=1)
        if start_date.weekday() < 5:
            count += 1
    return start_date