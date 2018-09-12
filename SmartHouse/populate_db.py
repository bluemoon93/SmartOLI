#!/usr/bin/python

from socket import *
import random
import numpy
import json

HOST = '10.1.0.129'  # All available interfaces
PORT = 5000  # The server port
s = socket(AF_INET, SOCK_STREAM)  # create a TCP socket
s.connect((HOST, PORT))  # connect to server on the port

for day in [5, 6, 7, 8, 9]:
    for i in range(50):
        l = [("ph", round(max(min(numpy.random.normal(7, 4), 13), 2)),2),
             ("flush", random.randint(1, 2)),
             ("level", max(min(numpy.random.normal(12, 2), 25), 15))]

        obj = {"type": "store_val",
               "device_id": random.randint(1, 3),
               "date": '2018-09-' + ("%02d" % day) + ' ' + ("%02d" % random.randint(0, 23)) + ':' + ("%02d" %
                   random.randint(0, 59)) + ':' + ("%02d" % random.randint(0, 59)),
               "sensors": l}

        s.send(json.dumps(obj) + "\n\n")  # send the data
        print('send--> ' + str(obj))
exit()
for day in [5, 6, 7]:
    for i in range(5):
        l = [("ph", max(min(numpy.random.normal(7, 4), 13), 2)),
             ("flush", random.randint(1, 2)),
             ("level", max(min(numpy.random.normal(20, 2), 25), 15))]

        obj = {"type": "store_val",
               "device_id": random.randint(1, 20),
               "date": '2018-09-' + ("%02d" % day) + ' ' + ("%02d" % random.randint(0, 23)) + ':' + ("%02d" %
                   random.randint(0, 59)) + ':' + ("%02d" % random.randint(0, 59)),
               "sensors": l,
               "user_id": 2}

        s.send(json.dumps(obj) + "\n\n")  # send the data
        print('send--> ' + str(obj))

s.close()