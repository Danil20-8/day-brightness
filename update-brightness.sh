#!/bin/bash
cd "$(dirname "$0")"

# 1. Проверяем состояние крышки ноутбука
LID_STATE=$(cat /proc/acpi/button/lid/*/state)

if [[ $LID_STATE == *"closed"* ]]; then
    echo "Крышка закрыта. Скрипт не запущен."
    exit 0
fi

# 2. Быстрая проверка: не погас ли экран (работает от root за <1 мс)
# card*-eDP-1 — это стандартное имя встроенного монитора ноутбука в Ubuntu
if grep -q "disabled" /sys/class/drm/card*-eDP-1/enabled 2>/dev/null; then
    echo "Экран выключен или ноутбук в режиме сна. Пропускаю автояркость."
    exit 0
fi

# 3. Дополнительная проверка на случай, если яркость уже на нуле
if [ -d /sys/class/backlight ] && [ "$(cat /sys/class/backlight/*/brightness 2>/dev/null | head -n 1)" -eq 0 ]; then
    echo "Подсветка экрана отключена (яркость 0). Пропускаю автояркость."
    exit 0
fi

# 4. Если все проверки пройдены, запускаем основной скрипт
echo "Крышка открыта, экран активен. Запускаю скрипт яркости..."
python3 get-nice-brightness.py
