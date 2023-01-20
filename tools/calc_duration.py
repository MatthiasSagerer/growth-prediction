from datetime import datetime
import time


def currentDateTime(txt='Current date and time'):
    today = datetime.today()
    today_str = today.strftime('%d/%m/%Y, %H:%M:%S')

    return f'{txt}: {today_str}', today


def calculateDuration(start_point, end_point):
    duration = end_point - start_point
    return duration
