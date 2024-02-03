import my_serial as messager
import time

portx = '/dev/tty.usbserial-130'
ser = messager.serial_init(portx)
while True:
    messager.send_enemy_location(ser, 3, 100000 / 1000, 100000 / 1000)  # mm to m
    time.sleep(0.5)