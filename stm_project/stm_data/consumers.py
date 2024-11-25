from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import serial_asyncio

class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Open serial port and stream data
        self.serial_task = asyncio.create_task(self.read_serial())

    async def disconnect(self, close_code):
        if self.serial_task:
            self.serial_task.cancel()

    async def read_serial(self):
        try:
            reader, _ = await serial_asyncio.open_serial_connection(url='/dev/ttyUSB0', baudrate=9600)
            while True:
                line = await reader.readline()
                if line:
                    data = line.decode('utf-8').strip().split(',')
                    await self.send_json({
                        'temperature': data[0],
                        'motion': data[1],
                        'light_intensity': data[2],
                        'curtains_drawn': data[3],
                        'lcd_message': data[4]
                    })
        except Exception as e:
            print(f"Serial error: {e}")
