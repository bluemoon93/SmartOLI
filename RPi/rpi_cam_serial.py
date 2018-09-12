from picamera import PiCamera
import socket
import serial
import time
import json
import datetime
import os

camera = PiCamera()

ser0 = serial.Serial("/dev/ttyUSB0", 9600)
ser0.flushInput()

try:
    ser1 = serial.Serial("/dev/ttyUSB1", 9600)

    # Send trash, its necessary for some reason
    ser1.write('.')
    ser1.write('.')
    ser1.write('.')
except:
    print("Second Arduino not found. Re-hashing")
    ser1 = ser0
ser1.flushInput()

iot_ip = '10.1.0.129'  # All available interfaces
iot_port = 5000  # The server port
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a TCP socket
    s.connect((iot_ip, iot_port))  # connect to server on the port
except:
    print("Couldn't connect to IoT")

this_device_id = 21
user_id = 2


def leds_off():
    ser1.write('D')
    ser1.flush()


def small_flush():
    ser1.write('A')
    ser1.flush()


def big_flush():
    ser1.write('B')
    ser1.flush()


def publish_flush(type_):
    try:
        obj = {"type": "store_val",
               "device_id": this_device_id,
               "date": str(datetime.datetime.now()).split(".")[0],
               "sensors": [("flush", type_)],
               "user_id": user_id}

        s.send(json.dumps(obj) + "\n\n")  # send the data
        print('Publishing flush ' + str(obj))
    except:
        print("Couldn't publish flush")


def publish_led(on):
    try:
        obj = {"type": "store_val",
               "device_id": this_device_id,
               "date": str(datetime.datetime.now()).split(".")[0],
               "sensors": [("led", 1 if on else 0)],
               "user_id": user_id}

        s.send(json.dumps(obj) + "\n\n")  # send the data
        print('Publishing led ' + str(obj))
    except:
        print("Couldn't publish led")


def open_lid_leds_on():
    ser1.write('F')
    ser1.flush()
    ser1.write('G')
    ser1.flush()
    time.sleep(18)


def close_lid():
    ser1.write('H')
    ser1.flush()
    #ser1.write('led 50\n')
    time.sleep(18)


def publish_water_level(val):
    try:
        obj = {"type": "store_val",
               "device_id": this_device_id,
               "date": str(datetime.datetime.now()).split(".")[0],
               "sensors": [("level", val)],
               "user_id": user_id}

        s.send(json.dumps(obj) + "\n\n")  # send the data
        print('Publishing level ' + str(obj))
    except:
        print("Couldn't publish level")


def publish_ph(val):
    try:
        obj = {"type": "store_val",
               "device_id": this_device_id,
               "date": str(datetime.datetime.now()).split(".")[0],
               "sensors": [("ph", val)],
               "user_id": user_id}

        s.send(json.dumps(obj) + "\n\n")  # send the data
        print('Publishing pH ' + str(obj))
    except:
        print("Couldn't publish pH")


def judge_with_nn():
    camera.capture('/home/pi/image.jpg')

    try:
        s = socket.socket()
        s.connect(("10.42.0.1", 6666))
        f = open('/home/pi/image.jpg', "rb")
        statinfo = os.stat('/home/pi/image.jpg')
        l = f.read(statinfo.st_size)

        info = str(statinfo.st_size)
        while len(info) < 20:
            info += " "
        s.send(info)

        # s.send(l)
        totalsent = 0
        while totalsent < statinfo.st_size:
            sent = s.send(l[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

        chunk = s.recv(1)
        if chunk == '':
            raise RuntimeError("socket connection broken")
        s.close()
    except:
        print("Couldn't connect to NN")
        return 2

    return int(chunk)


last_activity_detected_time = 0
last_flush_time = 0
bowl_open = False

ser0.flushInput()
ser0.readline()
print("Ready...")

while True:
    linein0 = ser0.readline().split(";")

    # someone here
    if float(linein0[1]) < 100:
        if not bowl_open:
            print("Opening @ " + linein0[0])
            open_lid_leds_on()
            publish_led(True)
            bowl_open = True
            print("Done")
        last_activity_detected_time = time.time()
        ser0.flushInput()
        ser0.readline()
        continue

    # flush!
    if float(linein0[0]) < 15 and bowl_open:
        print("Closing @ " + linein0[0])
        close_lid()
        bowl_open = False
        publish_water_level(float(linein0[2]))
        publish_ph(float(linein0[3]))

        # detect
        whats_in_the_bowl = judge_with_nn()
        leds_off()
        publish_led(False)

        if whats_in_the_bowl != 2:
            small_flush()
            publish_flush(1)
            print("Small flush")
        else:
            big_flush()
            publish_flush(2)
            print("Big flush")

        last_flush_time = time.time()
        print("Done")
        ser0.flushInput()
        ser0.readline()
        continue

    # if timeout (10s) and button hasnt been pressed
    if time.time() - last_activity_detected_time > 10 and \
                    last_activity_detected_time > last_flush_time and bowl_open:

        print("Timed-out!")
        close_lid()
        bowl_open = False

        # detect
        whats_in_the_bowl = judge_with_nn()
        leds_off()
        publish_led(False)

        if whats_in_the_bowl == 1:
            small_flush()
            print("Small flush")
        elif whats_in_the_bowl == 2:
            big_flush()
            print("Big flush")
        else:
            # empty, no flush
            print("No flush")
        print("Done")
        ser0.flushInput()
        ser0.readline()
        continue

    # Done!
    pass

print("Over.")
s.close()
ser1.close()
ser2.close()
