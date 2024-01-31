import subprocess
import os
import time
import threading
import paho.mqtt.client as mqtt
import base64
import keyboard
from io import BytesIO
from PIL import Image
from tkinter import filedialog
import tkinter as tk

MQTT_BROKER_ADDR = 'rjrietdijk.com'
MQTT_BROKER_PORT = 1883
MQTT_USERNAME = 'ie_minor'
MQTT_PASSWORD = 'wieditleesttrekteenbak'
# Print settings
DPI = 300
W_IN = 4
H_IN = 6

processing_image = False
print_image = None
print_thread = None
enable_printing = True

client = mqtt.Client(client_id=f"DELPHI-printer{time.time()}")
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("DELPHI/system_1/image_data")
    client.subscribe("DELPHI/system_1/state")

def on_message(client, userdata, msg):
    global processing_image, print_image, print_thread, enable_printing
    print(f"Message received on topic {msg.topic}")
    if msg.topic == 'DELPHI/system_1/image_data':
        processing_image = True
        try:
            payload_str = msg.payload.decode('utf-8')
            if payload_str.startswith('data:image/png;base64,'):
                image_data_base64 = payload_str.split(',')[1]
                image_data = base64.b64decode(image_data_base64)

                current_directory = os.path.dirname(os.path.abspath(__file__))
                raw_image_path = os.path.join(current_directory, 'raw_image.png')
                output_image_path = os.path.join(current_directory, 'print_processed.png')

                with open(raw_image_path, 'wb') as file:
                    file.write(image_data)

                with Image.open(BytesIO(image_data)) as image:
                    preprocess_print(image, output_image_path)
                    print_image = output_image_path
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            processing_image = False
    if enable_printing and msg.topic == 'DELPHI/system_1/state' and msg.payload.decode('utf-8') == 'printing':
        if print_thread is not None:
            return
        print_thread = threading.Thread(target=handle_printing)
        print_thread.start()

def handle_printing():
    global print_image, print_thread
    while processing_image:
        time.sleep(1)
    if print_image:
        process_print(print_image)
        time.sleep(60)
    print_thread = None

def execute_command(command):
    subprocess.Popen(
        command, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.STDOUT
    )

def select_irfanview_executable():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select IrfanView Executable (i_view64.exe)",
        filetypes=[("Executable Files", "*.exe")]
    )

    if file_path:
        return file_path
    else:
        return None

irfanview_path = select_irfanview_executable()

if irfanview_path and os.path.isfile(irfanview_path):
    print(f"IrfanView executable selected: {irfanview_path}")
else:
    print("IrfanView executable not selected or not found.")


def on_key_event(e):
    if e.name == 'q':
        print("Closing connection...")
        client.disconnect()
        exit()
    if e.name == 'p':
        global enable_printing
        enable_printing = not enable_printing
        print(f'Printing is now {"enabled" if enable_printing else "disabled"}')

def resize_and_crop(image, output_path, page_dimensions):
    try:
        image.thumbnail(page_dimensions, Image.Resampling.LANCZOS)

        page_ratio = page_dimensions[0] / page_dimensions[1]
        img_ratio = image.width / image.height

        if img_ratio > page_ratio:
            new_height = page_dimensions[1]
            new_width = int(new_height * img_ratio)
        else:
            new_width = page_dimensions[0]
            new_height = int(new_width / img_ratio)

        img_resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        left = (new_width - page_dimensions[0]) / 2
        top = (new_height - page_dimensions[1]) / 2
        right = (new_width + page_dimensions[0]) / 2
        bottom = (new_height + page_dimensions[1]) / 2

        img_cropped = img_resized.crop((left, top, right, bottom))

        img_cropped.save(output_path, quality=95)
    
    except Exception as e:
        print(f"An error occurred: {e}")

def preprocess_print(image, output_image_path):
    page_size = (W_IN * DPI, H_IN * DPI)
    resize_and_crop(image, output_image_path, page_size)

def process_print(output_image_path):
    command = f'"{irfanview_path}" "{output_image_path}" /dpi=({DPI},{DPI}) /print'
    execute_command(command)

keyboard.on_press(on_key_event)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER_ADDR, MQTT_BROKER_PORT, 60)
client.loop_forever()