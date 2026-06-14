from .base import BrightnessDevice
import subprocess
import os

class LinuxIntelBrightnessDevice(BrightnessDevice):
    def __init__(self) -> None:
        with open('/sys/class/backlight/intel_backlight/brightness') as f: self.current_brightness = float(f.read())
        with open('/sys/class/backlight/intel_backlight/max_brightness') as f: self.max_brightness = float(f.read())
        self.min_brightness = self.max_brightness / 100
        
    def commit(self) -> None:
        if os.getuid() == 0:
            subprocess.run(["sh", "-c", f"echo {int(self.current_brightness)} | tee /sys/class/backlight/intel_backlight/brightness"])
        else:
            subprocess.run(["sh", "-c", f"echo {int(self.current_brightness)} | sudo tee /sys/class/backlight/intel_backlight/brightness"])
        # with open("/sys/class/backlight/intel_backlight/brightness", "w") as text_file:
        #     text_file.write(str(int(self.current_brightness)))