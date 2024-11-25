import serial
from .models import SensorData

def read_serial_data(port='/dev/ttyUSB0', baudrate=9600):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line:
                # Assuming the STM32 sends comma-separated values like:
                # "25.5,1,3000,0,Hello World"
                data = line.split(',')
                if len(data) == 5:
                    SensorData.objects.create(
                        temperature=float(data[0]),
                        motion=bool(int(data[1])),
                        light_intensity=int(data[2]),
                        curtains_drawn=bool(int(data[3])),
                        lcd_message=data[4]
                    )
    except serial.SerialException as e:
        print(f"Serial error: {e}")
