import mouse, sys
import serial
import time

arduino = serial.Serial(port='COM4',   baudrate=115200, timeout=.1)

mouse.FAILSAFE = False


def write_read():
    # time.sleep(0.005)
    data = arduino.readline()
    return   data

clicked = False
modeClicked = False
active = True

while True:
    try:

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

            # if not active:
            #     continue

            # move mouse

            (mouseX, mouseY) = mouse.get_position()
            mouse.move(mouseX + x/500, mouseY + y/500, absolute=True, duration=0)

            # mouse click
            if click and not clicked:
                clicked = True
                # Press down left Mouse btn
                mouse.press(mouse.LEFT)
            if not click and clicked:
                clicked = False
                # Release left Mouse btn
                mouse.release(mouse.LEFT)
                

    except KeyboardInterrupt:
        print("bye")
        break
    except Exception as e:
        print(e)
