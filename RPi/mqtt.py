from time import sleep
from adafruit import get_adafruit_key
from gtts import gTTS
import os

aio = get_adafruit_key()  # Secret key, not available in repo
data = aio.receive('smartoli')
prev_data = data.value
sleep(1)


def talktome(audio):
    print(audio)
    tts = gTTS(text=audio, lang='en')
    tts.save('temp.mp3')  # install mpg123 Audio Player Software
    os.system('mpg123 temp.mp3')


def start_audio():
    os.system('mpg123 trap.mp3 &')


def stop_audio():
    os.system('killall -9 mpg123')

# Print the value if there is a change Notice that the value is
# converted from string to int because it always comes back as a string from IO.
while True:
    data = aio.receive('smartoli')

    if data.value == prev_data:
        sleep(1)
        continue

    prev_data = data.value
    #date = " ".join(str(data.value).split(" ")[0:5])
    split_text = str(data.value).split(" ")[5:]
    text = " ".join(split_text)
    #print("Got: "+text+" @ "+date)

    if "hello" in split_text or "hi" in split_text or "howdy" in split_text:
        talktome("Hello!")
    elif "stop" in split_text or "silence" in split_text or "quiet" in split_text:
        stop_audio()
        talktome("Stopping music...")
    elif "play" in split_text or "music" in split_text or "song" in split_text:
        talktome("Playing music...")
        start_audio()
    else:
        talktome("Unrecognized command")

    sleep(1)
