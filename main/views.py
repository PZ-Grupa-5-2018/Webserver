from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .models import Monitor
from .utils import getMonitorDataFromUrl
from .utils import getLastMeasurements
from django.core import serializers
import json


def downloadMonitorDetails(request, monitor_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    monitor_data = getMonitorDataFromUrl(monitor_url)
    parsed = json.loads(json.dumps(monitor_data))
    response = HttpResponse(json.dumps(parsed, indent=4, sort_keys=True), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename='+'monitor_'+str(monitor_url)+'_data.json'

    return response

def index(request):
    menu_list = [{'name': 'monitor list', 'url': '/monitors'}, {'name': 'login', 'url': '/login'}]
    context = {
        'menu_list': menu_list,
    }
    return render(request, 'main/index.html', context)


def monitors(request):
    monitors = Monitor.objects.all()

    context = {
        'monitors': monitors,
    }
    return render(request, 'main/monitors.html', context)


def monitors_detail(request, monitor_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    url = str(monitor_url) + "/hosts/"
    response = requests.get(url)
    data = response.json()
    last_measurements = getLastMeasurements(monitor_id, 20)
    context = {
        'id': monitor_id,
        'url': monitor_url,
        'hosts': data,
        'last_measurements': last_measurements,
    }
    return render(request, 'main/monitors_detail.html', context)


def hosts_detail(request, monitor_id, host_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    url = str(monitor_url) + "/hosts/" + str(host_id) + "/"
    response = requests.get(url)
    host_data = response.json()

    url = url + "metrics/"
    response = requests.get(url)
    metrics_data = response.json()
    context = {
        'host_data': host_data,
        'metrics_data': metrics_data,
    }
    return render(request, 'main/host_detail.html', context)


def metrics_detail(request, monitor_id, host_id, metric_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    url = str(monitor_url) + "/hosts/" + str(host_id) + "/metrics/" + str(metric_id)
    response = requests.get(url)
    metric_data = response.json()

    url = url + "/measurements/"
    response = requests.get(url)
    measurements_data = response.json()
    context = {
        'metric_data': metric_data,
        'measurements_data': measurements_data,
    }
    return render(request, 'main/metrics_detail.html', context)


def login(request):
    context = {}
    return render(request, 'main/login.html', context)


def register(request):
    context = {}
    return render(request, 'main/register.html', context)
