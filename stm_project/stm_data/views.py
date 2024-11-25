from django.shortcuts import render

# Create your views here.
import csv
from django.utils.timezone import now
from .models import SensorData

# def parse_csv(file_path):
#     with open(file_path, 'r') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             SensorData.objects.create(
#                 temperature=float(row['Temperature']),
#                 motion=bool(int(row['Motion'])),
#                 light_intensity=int(row['Light Intensity']),
#                 curtains_drawn=bool(int(row['Curtains Drawn'])),
#                 lcd_message=row['LCD Message']
#             )
            
            
def sensor_data_view(request):
    data = SensorData.objects.all().order_by('-timestamp')
    return render(request, 'sensor_data.html', {'data': data})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SensorData
from .serializer import SensorDataSerializer

@api_view(['GET'])
def sensor_data_list(request):
    data = SensorData.objects.all().order_by('-timestamp')
    serializer = SensorDataSerializer(data, many=True)
    return Response(serializer.data)

# views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Template, Context
from pathlib import Path
import os
from django.conf import settings

def sensor_data_view(request):
    # Construct the path to the HTML template
    html_path = os.path.join(settings.BASE_DIR, 'stm_data', 'templates', 'sensor_data.html')
    
    with open(html_path, 'r') as f:
        template_content = f.read()
    
    template = Template(template_content)
    context = Context({})
    return HttpResponse(template.render(context))
