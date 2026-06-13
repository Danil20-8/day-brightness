import os
import cv2
import numpy as np
import time
from .exceptions import CameraReadError

webcam_config_path = os.path.join("config", "webcam")
webcam_config_last_path = os.path.join("config", "webcam", "last")

if not os.path.exists(webcam_config_path):
    os.makedirs(webcam_config_path)

def get_webcam_multiplier():
    webcam = cv2.VideoCapture(0)
    
    # Оптимизация параметров захвата
    webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   # Уменьшаем разрешение
    webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    webcam.set(cv2.CAP_PROP_BUFFERSIZE, 1)      # Уменьшаем буфер

    # Пропускаем 5 кадров для стабилизации
    for _ in range(5):
        webcam.read()
    
    def get_frame_value():
        # Используем один вызов waitKey
        cv2.waitKey(1)
        
        # Читаем кадр
        ret, frame = webcam.read()
        if not ret:
            raise CameraReadError("Не удалось получить кадр с веб-камеры")
        
        # Конвертируем в оттенки серого (более эффективно)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Создаем весовую матрицу один раз
        h, w = gray.shape
        center_y, center_x = h / 2, w / 2
        
        # Векторизованный расчет расстояний
        y, x = np.ogrid[:h, :w]
        dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        
        # Взвешенное среднее
        weighted_avg = np.average(gray, weights=dist)
        
        return float(weighted_avg)
    
    # Собираем 3 кадра с задержкой
    results = []
    for _ in range(1):
        results.append(get_frame_value())
        time.sleep(0.033)  # ~30 FPS, достаточно для стабильности
    
    result = np.mean(results)
    webcam.release()  # Освобождаем камеру
    
    # Чтение и запись последнего значения
    try:
        if os.path.exists(webcam_config_last_path):
            with open(webcam_config_last_path, "r+") as lastFile:
                lastFileValue = lastFile.readline().strip()
                if lastFileValue:
                    last_color = float(lastFileValue)
                    lastFile.seek(0)
                    lastFile.write(str(result))
                    lastFile.truncate()
                    return result / last_color if last_color != 0 else 1.0
                else:
                    lastFile.write(str(result))
                    return 1.0
        else:
            with open(webcam_config_last_path, "w") as lastFile:
                lastFile.write(str(result))
                return 1.0
    except (IOError, ValueError):
        return 1.0