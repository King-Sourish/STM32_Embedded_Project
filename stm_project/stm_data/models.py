from django.db import models


class SensorData(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()
    motion = models.BooleanField()
    light_intensity = models.IntegerField()
    curtains_drawn = models.BooleanField()
    lcd_message = models.TextField()


class CSVFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/')
