import mouse
import serial
import time
import threading
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

# Настройка Arduino
arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)

# Настройка громкости через pycaw
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Определение текущего уровня громкости
current_volume = volume.GetMasterVolumeLevelScalar()

# Начальные значения
clicked = False
modeClicked = False
active = True
change_volume = False  # Флаг для изменения громкости
direction = 0          # Направление изменения (-1 для уменьшения, 1 для увеличения)


def write_read():
    data = arduino.readline()
    return data


# Функция для плавного изменения громкости
def adjust_volume():
    global current_volume, change_volume, direction

    while True:
        if change_volume:
            # Изменение громкости на 1% в секунду
            current_volume = max(0.0, min(current_volume + (-direction * 0.01), 1.0))
            volume.SetMasterVolumeLevelScalar(current_volume, None)
            print(f"Current Volume: {current_volume * 100:.0f}%")
            time.sleep(0.25)  # Задержка в 1 секунду
        else:
            time.sleep(0.1)  # Проверка каждые 0.1 секунды, пока флаг выключен


# Запуск потока для управления громкостью
volume_thread = threading.Thread(target=adjust_volume, daemon=True)
volume_thread.start()

while True:
    try:
        # Чтение данных от Arduino
        value = write_read()
        arr = value.decode('ascii').replace("\r\n", "").split(":") if value else []

        if arr:
            x = -int(arr[0])
            y = -int(arr[1])
            click = True if arr[2] == "1" else False
            mode = True if arr[3] == "1" else False
            print(arr)

            if mode and not modeClicked:
                active = not active
                modeClicked = True
            if not mode and modeClicked:
                modeClicked = False

            # Проверка направления изменения громкости
            if y > 100:
                direction = 1  # Увеличение громкости
                change_volume = True
            elif y < -100:
                direction = -1  # Уменьшение громкости
                change_volume = True
            else:
                change_volume = False  # Остановка изменения громкости

            # Управление мышью (пример)
            # (mouseX, mouseY) = mouse.get_position()
            # mouse.move(mouseX + x / 500, mouseY + y / 500, absolute=True, duration=0)

            # Нажатие мыши
            if click and not clicked:
                clicked = True
                mouse.press(mouse.LEFT)
            if not click and clicked:
                clicked = False
                mouse.release(mouse.LEFT)

    except KeyboardInterrupt:
        print("Программа завершена.")
        break
    except Exception as e:
        print(e)
