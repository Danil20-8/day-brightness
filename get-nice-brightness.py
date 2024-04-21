import asyncio
from brightness_device.timer import TimerBrightnessDevice
from get_multiplier.time import get_time_multiplier
from get_multiplier.webcam import get_webcam_multiplier
from brightness_device.base import BrightnessDevice
from brightness_device.linux_intel import LinuxIntelBrightnessDevice

class DayBrightness():
    def __init__(self, device: BrightnessDevice):
        self.device = device
    
    def update_brightness(self):
        base_value = (self.device.current_brightness - self.device.min_brightness)

        self.device.set_brightness(self.device.min_brightness + base_value * get_webcam_multiplier())
        
        return
    

async def __main__():
    device = TimerBrightnessDevice(
        percent_per_second=15,
        frame_per_second=15,
        device=LinuxIntelBrightnessDevice()
    )

    day_brightness = DayBrightness(device)
    
    day_brightness.update_brightness()

    device.commit()
    
    await device.done()

loop = asyncio.get_event_loop()
loop.run_until_complete(__main__())