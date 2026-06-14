
from datetime import datetime
from math import sin,pi
from get_today_end_points.api import get_today_end_points


def get_time_multiplier():
    datEndPoints = get_today_end_points()
    begin_of_light_minute = datEndPoints.sunrise.hour * 60 + datEndPoints.sunrise.minute
    end_of_light_minute = datEndPoints.sunset.hour * 60 + datEndPoints.sunset.minute

    def count_sin(current_minute):
        minute_value = (current_minute if current_minute > begin_of_light_minute else current_minute + 24 * 60) - begin_of_light_minute
        bright_hours = (end_of_light_minute if end_of_light_minute > begin_of_light_minute else end_of_light_minute + 24 * 60) - begin_of_light_minute
        angle  = pi / bright_hours * minute_value

        return sin(angle)

    current_datetime = datetime.now()
    
    current_minute = current_datetime.hour * 60 + current_datetime.minute
    minute_step = 1

    previous_minute = current_minute - minute_step
    previous_minute = previous_minute + 24 * 60 if previous_minute < end_of_light_minute and end_of_light_minute < begin_of_light_minute else previous_minute
    previous_minute = previous_minute if previous_minute >= 0 else 24 * 60 - minute_step

    if not (previous_minute > begin_of_light_minute and previous_minute <= (end_of_light_minute if end_of_light_minute > begin_of_light_minute else end_of_light_minute + 24 * 60)):
        return 1.0
    
    previous_sin = count_sin(previous_minute)

    current_sin = count_sin(current_minute)

    return current_sin / previous_sin