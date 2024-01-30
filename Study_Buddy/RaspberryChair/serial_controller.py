import serial
import numpy as np
import time

# -- Serial configuration --
serial_port = '/dev/ttyACM0'
baud_rate = 9600

counter = 0
history = np.array([])
ser = serial.Serial(serial_port, baud_rate, timeout=1)

def get_serial_data(threshold):

    global counter
    global history

    try:
        if ser.is_open:
            
            # -- Get latest serial data
            data = None
            try:
                ser.flushInput()
                data = ser.readline().decode().strip()
            except:
                pass
        

            # -- Parse serial data
            parsed_data = None
            try:
                parsed_data = int(data)
            except:
                pass

            is_sitted = False

            if parsed_data:
                is_sitted = parsed_data < -80000

            '''
            # -- Append parsed serial data to history
            if parsed_data:
                history = np.append(history, parsed_data)

            # -- Check for sudden change in last data and past 10 
            is_sudden_change = False
            if len(history) > 10 and parsed_data:
                avg_points = np.mean(history)
                is_sudden_change = sudden_change(parsed_data, threshold)
            '''

            counter += 1
            if data:
                print(f'{counter}: {data} - user sitting: {is_sitted}')

            return data, is_sitted

    except serial.SerialException as e:
        pass
        return None

def sudden_change(sensor_data, threshold):
    global history
    
    window = 10

    avg_value = np.mean(history[-window + 1 : -1])
    diff = np.abs(sensor_data - avg_value)

    return diff > threshold
