from datetime import date, time

from .config import load_config, save_config
from .api_sunrisesunset_io import get_with_api_sunrisesunset_io

def get_today_end_points():
    today = date.today()
    
    try:
        table = get_table()
        
        sunriseTimeValues = list(map(lambda t: int(t), table[today.month][today.day]['sunrise'].split(':')))
        sunrise = time(sunriseTimeValues[0], sunriseTimeValues[1])

        sunsetTimeValues = list(map(lambda t: int(t), table[today.month][today.day]['sunset'].split(':')))
        sunset = time(sunsetTimeValues[0], sunsetTimeValues[1])
                       
        return DayEndPoints(sunrise, sunset)
    except Exception as e:
        return DayEndPoints(time(5, 0), time(9, 0))

class DayEndPoints:
    def __init__(self, sunrise: time, sunset: time):
        self.sunrise = sunrise
        self.sunset = sunset
    def __str__(self):
        return { 'sunrise': self.sunrise, 'sunset': self.sunset }.__str__()
        
def get_table():    
    table = load_config()

    if not table is None:
        return table
    
    table = get_with_api_sunrisesunset_io()

    save_config(table)

    return table