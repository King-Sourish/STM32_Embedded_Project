from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SensorData

@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'temperature', 'motion', 'light_intensity', 'curtains_drawn', 'lcd_message')
