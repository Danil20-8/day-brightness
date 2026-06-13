from .base import BrightnessDevice
import asyncio

class TimerBrightnessDevice(BrightnessDevice):
    process: asyncio.Task
    def __init__(self, percent_per_second: float, frame_per_second: float, device: BrightnessDevice) -> None:
        self.process = None
        self.percent_per_second = percent_per_second
        self.frame_per_second = frame_per_second
        self.device = device
        self.max_brightness = device.max_brightness
        self.min_brightness = device.min_brightness
        self.current_brightness = device.current_brightness
        pass

    def commit(self) -> None:
        async def run_brightness_change():
            nonlocal self
            
            while(1):
                direction = -1 if self.current_brightness < self.device.current_brightness else 1

                next_brightness = (
                    max(
                        min(
                            self.device.current_brightness + (self.max_brightness / 100 * self.percent_per_second / self.frame_per_second * (direction)),
                            self.max_brightness if direction < 0 else self.current_brightness
                        ),
                        self.min_brightness if direction > 0  else self.current_brightness
                    )
                )
                
                self.device.set_brightness(next_brightness)
                self.device.commit()
                if(self.device.current_brightness == self.current_brightness):
                    self.process = None
                    return
                else:
                    await asyncio.sleep(1 / self.frame_per_second)

        self.process = asyncio.create_task(run_brightness_change())

    async def done(self) -> None:
        if(self.process != None):
            await self.process
        return