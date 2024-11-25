from django.core.management.base import BaseCommand
from stm_data.serial_reader import read_serial_data

class Command(BaseCommand):
    help = 'Read data from STM32 board via serial'

    def handle(self, *args, **kwargs):
        read_serial_data(port='COM4', baudrate=115200)
