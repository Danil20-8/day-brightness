import json
import os

from state_dir import get_state_file
from .base import BrightnessDevice

class HdrBrightnessDevice(BrightnessDevice):
    def __init__(self, device: BrightnessDevice) -> None:
        self.device = device
        self.max_brightness = device.max_brightness
        self.min_brightness = device.min_brightness
        self.current_brightness = restore_hdr_value(device.current_brightness)

    def set_brightness(self, brightness: float) -> None:
        self.current_brightness = brightness

    def commit(self) -> None:
        device_brightness = self._clamp_to_device_range(self.current_brightness)
        self.device.set_brightness(device_brightness)

        remember_hdr_value(self.current_brightness)  # передаём только HDR значение

        self.device.commit()

    def _clamp_to_device_range(self, hdr_value: float) -> float:
        return max(self.device.min_brightness, 
                   min(self.device.max_brightness, hdr_value))


def remember_hdr_value(hdr_value: float) -> None:
    """Сохраняет только текущее HDR значение, перезаписывая файл (энергоэффективно)"""
    config_file = get_state_file("hdr")
    
    # Пишем напрямую, без чтения предыдущих значений
    try:
        with open(config_file, 'w') as f:
            json.dump(hdr_value, f)  # сохраняем только одно число
    except IOError:
        pass  # игнорируем ошибки записи для экономии энергии


def restore_hdr_value(default_value: float) -> float:
    """Восстанавливает последнее сохранённое HDR значение"""
    config_file = get_state_file("hdr")
    
    if not os.path.exists(config_file):
        return default_value
    
    try:
        with open(config_file, 'r') as f:
            return json.load(f)  # читаем одно число
    except (json.JSONDecodeError, IOError, TypeError):
        return default_value