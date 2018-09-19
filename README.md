# SmartOLI

## Sunset Hackathon 2018

![image](https://user-images.githubusercontent.com/9117323/45421508-2ad04d00-b685-11e8-84bd-1d0b20295b22.png)

A smart toilet, fully integrated with [OLI](https://www.oli-world.com/) products, that detects users, allows for hands-off interaction, chooses the appropriate flush, is integrated with Smartphone Assistants and SmartHouse systems, and has maintenance feedback and automatic filter cleaning protocols.

Demonstration videos and presentation available on the "Media" folder.

### Image Classification

Ready things with

    virtualenv venv
    pip install -r ../requirements.txt

Get some images into the "dataset_raw" folder. We used `crawl.py` and `google_bulk.sh` to get a dataset. If RPi is enabled, running `rpi_cam_batch.py` there to save a stream of images, and `cp_from_pi.sh` to copy them locally, also works. Then, `augment.py` to turn your small dataset into something large (we did 5k images per raw dataset category, and grouped into categories `pee`, `poo`, and `empty` in the "dataset" folder). Then, `learn.sh` to learn from the dataset, and test with `test.sh` (put test images in the "test" folder). 

During demonstration, `classify_server.py` is running (10.42.0.1:6666) to take calls from RPi and reply correct type.

### Sensor Arduino

Using 2 UltraSound sensors HC-SR04 (one for user detection on digital pins 9 & 10, one for deposit water level on digital pins 11 & 12), an InfraRed sensor GP2Y0A21 on analog pin 0, and a Temperature sensor DS18B20 (should have been pH, but we couldn't get one) on analog pin 2, the `AnalogSensors.ino` script reads all sensors and sends them to the serial connection as `ir;us0;us1;temp;\n`.

To install libraries, either get them directly from Arduino IDE, or follow [this](https://create.arduino.cc/projecthub/TheGadgetBoy/ds18b20-digital-temperature-sensor-and-arduino-9cc806).

### Actuator Arduino

The `Motors.ino` script receives commands from the RPi through the serial connection and acts upon the SmartOLI servos and motors. The protocol is based on single `char`s, as seen below.

- `A` Half flush
- `B` Full flush
- `C` End flush		// Debug
- `D` Led 0
- `E` Led 50
- `F` Led 100
- `G` Lid Up
- `H` Lid Down
- `J` Lid STOP		// Debug
- `X` Clean filter
- `Y` Reserve tank ON

The `Valves.ino` script acts upon the electrovalve system we developed to automatically clear the water filters in the SmartOLI. Check "Media/hack_2.wmv" for more info.

### SmartHouse Integration

<todo>

Check "Media/hack_1.wmv" for more info.

### RPi

To save batches of images from camera, run `rpi_cam_batch.py`.

To answer requests sent by Google Assistant via [IFTTT](https://ifttt.com) into an Adafruit MQTT server, keep `mqtt.py` running, and plug some speakers into the RPi.

During demonstration, first plug in the USB serial connecter to the Sensor Arduino (/dev/ttyUSB0), then the one to the Actuator Arduino (/dev/ttyUSB1), run the NN server (10.42.0.1:6666), and the SmartHouse server (10.1.0.129:5000). Finally, run `rpi_cam_serial.py` to process all the information from sensors, and execute upon actuators. The sensor arduino is required for this, the others are optional (NN's default to type 2, SmartHouse statistics are not sent, and actuators are not performed upon).

Check "Media/hack_0.wmv" for more info.