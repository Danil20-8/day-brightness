from get_multiplier.time import get_time_multiplier
from get_multiplier.webcam import get_webcam_multiplier
import sys

class BrightnessDevice():
    def __init__(self, current_brightness: float, absolute_min_brightness: float, absolute_max_brightness: float):
        self.current_brightness = current_brightness
        self.absolute_min_brightness = absolute_min_brightness
        self.absolute_max_brightness = absolute_max_brightness

    def set_brightness(self, brightness: float):
        self.current_brightness = brightness

    def commit(self):
        print(int(
            min(
                self.absolute_max_brightness,
                max(self.absolute_min_brightness, self.current_brightness)
                )
                )
            )

class DayBrightness():
    def __init__(self, device: BrightnessDevice):
        self.device = device
    
    def update_brightness(self):
        base_value = (self.device.current_brightness - self.device.absolute_min_brightness)

        self.device.set_brightness(self.device.absolute_min_brightness + base_value * get_webcam_multiplier())
        
        return
    

def __main__():
    current_brightness = float(sys.argv[1]) if len(sys.argv) > 0 else 3000
    absolute_max_brightness = float(sys.argv[2]) if len(sys.argv) > 1 else 19200
    absolute_min_brightness = absolute_max_brightness / 100

    device = BrightnessDevice(current_brightness, max(absolute_min_brightness, absolute_max_brightness * .01), absolute_max_brightness)

    day_brightness = DayBrightness(device)
    
    day_brightness.update_brightness()

    device.commit()

__main__()