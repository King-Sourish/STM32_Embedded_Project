# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import serial
import serial_asyncio
import logging

logger = logging.getLogger(__name__)

# class SensorDataConsumer(AsyncWebsocketConsumer):

# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
import asyncio
import serial_asyncio
import logging

logger = logging.getLogger(__name__)

class SensorDataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.info("New WebSocket connection attempt")
        try:
            await self.accept()
            logger.info("WebSocket connection accepted")
            self.serial_task = asyncio.create_task(self.read_serial())
        except Exception as e:
            logger.error(f"Error in connect: {e}")
            await self.close()

    async def disconnect(self, close_code):
        logger.info(f"WebSocket disconnected with code: {close_code}")
        if hasattr(self, 'serial_task'):
            self.serial_task.cancel()
            try:
                await self.serial_task
            except asyncio.CancelledError:
                pass

    async def read_serial(self):
        retry_count = 0
        max_retries = 5
        
        while retry_count < max_retries:
            try:
                reader, _ = await serial_asyncio.open_serial_connection(
                    url='COM4',
                    baudrate=115200
                )
                logger.info("Serial connection established")
                retry_count = 0  # Reset retry count on successful connection
                
                while True:
                    line = await reader.readline()
                    if line:
                        try:
                            data = line.decode('utf-8').strip().split(',')
                            await self.send(json.dumps({
                                'temperature': float(data[0]),
                                'motion': bool(int(data[1])),
                                'light_intensity': int(data[2]),
                                'curtains_drawn': bool(int(data[3])),
                                'lcd_message': data[4]
                            }))
                        except (IndexError, ValueError) as e:
                            logger.error(f"Error parsing serial data: {e}")
                            continue
                            
            except Exception as e:
                retry_count += 1
                logger.error(f"Serial connection error (attempt {retry_count}/{max_retries}): {e}")
                await asyncio.sleep(2 ** retry_count)  # Exponential backoff
                
        logger.error("Max retries reached for serial connection")