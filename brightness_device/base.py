from abc import ABC, abstractmethod

class BrightnessDevice(ABC):
    current_brightness: float
    max_brightness: float
    min_brightness: float

    def set_brightness(self, brightness: float) -> None:
        self.current_brightness = max(self.min_brightness, min(self.max_brightness, brightness))

    @abstractmethod        
    def commit(self) -> None:
        pass