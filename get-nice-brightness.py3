import datetime
from math import sin,cos, pi
import sys

class BrightnessDevice():
    def __init__(self, current_brightness: float, absolute_min_brightness: float, absolute_max_brightness: float):
        self.current_brightness = current_brightness
        self.absolute_min_brightness = absolute_min_brightness
        self.absolute_max_brightness = absolute_max_brightness

    def set_brightness(self, brightness: float):
        self.current_brightness = brightness

    def commit(self):
        print(int(self.current_brightness))

class DayBrightness():
    begin_of_light_hour = 5
    end_of_light_hour = 22

    def __init__(self, device: BrightnessDevice):
        self.device = device
    
    def update_brightness(self, current_hour: float):
        # min_brightness = max(absolute_min_brightness, absolute_max_brightness * .1)
        # max_brightness = absolute_max_brightness * .7

        previous_hour = current_hour - 1
        previous_hour = previous_hour if previous_hour > 0 else 23

        # print((previous_hour, self.begin_of_light_hour, (self.end_of_light_hour if self.end_of_light_hour > self.begin_of_light_hour else self.end_of_light_hour + 24)))

        if not (previous_hour > self.begin_of_light_hour and previous_hour <= (self.end_of_light_hour if self.end_of_light_hour > self.begin_of_light_hour else self.end_of_light_hour + 24)):
            self.device.set_brightness(self.device.current_brightness)
            return

        previous_sin = self.count_sin(previous_hour)

        current_sin = self.count_sin(current_hour)

        # print((previous_sin, current_sin))

        self.device.set_brightness(
            int(
                min(
                    max(
                        self.device.absolute_min_brightness,
                        self.device.current_brightness / previous_sin * current_sin
                        ),
                    self.device.absolute_max_brightness
                    )
                )
        )

    def count_sin(self, current_hour):

        hour_value = (current_hour if current_hour > self.begin_of_light_hour else current_hour + 24) - self.begin_of_light_hour

        bright_hours = (self.end_of_light_hour if self.end_of_light_hour > self.begin_of_light_hour else self.end_of_light_hour + 24) - self.begin_of_light_hour

        angle  = pi / bright_hours * hour_value

        # print((hour_value, bright_hours, sin(angle), sin(pi / 2)))

        return sin(angle)
    

def __main__():
    current_brightness = float(sys.argv[1]) if len(sys.argv) > 0 else 3000

    absolute_min_brightness = 192
    absolute_max_brightness = 19200

    device = BrightnessDevice(current_brightness, max(absolute_min_brightness, absolute_max_brightness * .1), absolute_max_brightness)

    day_brightness = DayBrightness(device)

    current_hour = datetime.datetime.now().hour
    
    day_brightness.update_brightness(current_hour)

    device.commit()

    # for i in range(0, 24):
    
    #     day_brightness.update_brightness(14)

    #     device.commit()
# print_brightness(14, 3000, max(absolute_min_brightness, absolute_max_brightness * .1), absolute_max_brightness)

# print(sin(pi) * 1234)

# print(sys.argv[1])

__main__()