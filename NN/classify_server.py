#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tensorflow as tf
import sys
import os
import csv
import socket
import threading
from time import sleep
from PIL import ImageTk
from tkinter import *
from PIL import Image

# Disable tensorflow compilation warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class Application(Frame):
    def __init__(self, root):
        w, h = 720, 500
        root.geometry("%dx%d+0+0" % (w, h))

        Frame.__init__(self, root, background="#000000", cursor='none')
        self.root = root
        self.pack()
        self.canvas = Canvas(self, width=720, height=500, borderwidth=0, background="#FFFFFF")
        self.canvas.pack(side="top")

        self.title = Label(self.canvas, text="Loading...", background="#FFFFFF", foreground="#000000")
        self.title.pack(side="top")

        image = Image.open('temp.jpg')
        self.photo = ImageTk.PhotoImage(image)
        self.photo_container = Label(self.canvas, image=self.photo)
        self.photo_container.pack(side="top")

        self.thread = threading.Thread(target=main, args=(self,))
        self.thread.start()


end = False


def main(app):
    # create an INET, STREAMing socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversocket.bind(('10.42.0.1', 6666))
    serversocket.listen(1)
    serversocket.settimeout(1)

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("trained_model/retrained_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("trained_model/retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        print("Waiting...")
        app.title.config(text='Waiting...')

        while end is False:
            # accept connections from outside


            try:
                (clientsocket, address) = serversocket.accept()
            except:
                # print("timeout")
                continue
            # now do something with the clientsocket

            temp_file = open("temp.jpg", 'wb')  # Open in binary
            bytes_recd = 0

            msg_size = clientsocket.recv(20)
            if msg_size == '':
                print("socket connection broken")
                continue
            # print(msg_size.strip(), int(msg_size.strip()))
            msg_size = int(msg_size.strip())

            # chunks = []
            bytes_recd = 0
            while bytes_recd < msg_size:
                chunk = clientsocket.recv(min(msg_size - bytes_recd, msg_size))
                # print(".")
                if chunk == '':
                    print("socket connection broken")
                    continue
                # chunks.append(chunk)
                temp_file.write(chunk)
                bytes_recd = bytes_recd + len(chunk)

            # f.write(chunks)
            temp_file.close()
            app.photo = ImageTk.PhotoImage(Image.open('temp.jpg'))
            app.photo_container.config(image=app.photo)
            # image = Image.open('temp.jpg')
            # image.show()

            # Read the image_data
            image_data = tf.gfile.FastGFile("temp.jpg", 'rb').read()

            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            predictions = sess.run(softmax_tensor,
                                   {'DecodeJpeg/contents:0': image_data})

            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            row_dict = {}

            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                row_dict[human_string] = score

            print(row_dict)
            app.title.config(
                text="Type 1 - %4.2f%% || %4.2f%% - Type 2" % (row_dict["pee"] * 100, row_dict["poo"] * 100))

            # 50% or more chance of poo, lets say poo
            clientsocket.send("2" if row_dict['poo'] > 0.4 else ("1" if row_dict['pee'] > 0.4 else "0"))
            clientsocket.close()
            print("Waiting...")

        f.close()

    serversocket.close()
    if end is False:
        app.root.destroy()


def on_closing():
    global end
    end = True
    app.root.destroy()


if __name__ == '__main__':
    root = Tk()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = Application(root)
    try:
        root.mainloop()
    except KeyboardInterrupt:
        end = True
        app.root.destroy()
