from datetime import date, datetime, timedelta
import time
import requests
import dateutil.parser

from .get_coordinates.ip_api_com import get_with_ip_api_com

def get_with_api_sunrisesunset_io():
    today = date.today()

    [latitude, longitude] = get_client_coordinates()

    url = f"https://api.sunrisesunset.io/json?lat={latitude}&lng={longitude}&date_start={today.year}-01-01&date_end={today.year}-12-31"

    result = requests.get(url).json()

    table = {}

    time_offset = time.altzone / -60

    for day in result['results']:
        day_date = dateutil.parser.parse(day['date'])
        if not day_date.month in table:
            table[day_date.month] = {}

        table[day_date.month][day_date.day] = { 
            'sunrise': (datetime.strptime(day['sunrise'], '%I:%M:%S %p') + timedelta(minutes= time_offset - day['utc_offset'])).strftime('%H:%M'),
            'sunset': (datetime.strptime(day['sunset'], '%I:%M:%S %p') + timedelta(minutes= time_offset - day['utc_offset'])).strftime('%H:%M')
         }

    return table

def get_client_coordinates():
    return get_with_ip_api_com()