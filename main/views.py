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
import datetime
import time

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

    data_chart = []
    for metric in metrics_data:
        url = str (monitor_url) + "/hosts/" + str (host_id) + "/metrics/" + str (metric["id"]) + "/measurements"
        response = requests.get (url)
        measurements_data = response.json ()
        values = []
        for single_measurment in measurements_data:
            values.append ( { 'x': time.mktime (
                datetime.datetime.strptime (single_measurment["timestamp"], "%Y-%m-%dT%H:%M:%SZ").timetuple ()), 'y': single_measurment["value"]})
        data_chart.append (dict (key=metric["type"], values=values))

    context = {
        'host_data': host_data,
        'metrics_data': metrics_data,
        'chart_data': json.dumps(data_chart),
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


def search(request):
    context = {}
    return render(request, 'main/search.html', context)


def search_host(request):
    # 'generic' jak wyszukujemy globalnie, 'advanced' jak z urla /search
    search_type = request.GET['search_type']
    monitor = Monitor.objects.all()

    try:
        cpu = request.GET['CPU']
    except:
        cpu = "off"

    try:
        ram = request.GET['RAM']
    except:
        ram = 'off'

    try:
        hdd = request.GET['HDD']
    except:
        hdd = 'off'

    if search_type == 'generic':
        all_metric_data = []
        for i in monitor:
            url = i.url
            url = url + '/hosts/?format=json'
            name = request.GET['search_generic']
            url = url + '&name=' + name

            response = requests.get(url)
            metric_data = response.json()
            for j in metric_data:
                j['monitor_id'] = i.id
                j['monitor_url'] = i.url

            all_metric_data.extend(metric_data)

        context = {
            'data': all_metric_data,
        }
        return render(request, 'main/search_host.html', context)

    else:
        all_metric_data = []
        for i in monitor:
            url = i.url
            url = url + '/hosts/?format=json'
            name = request.GET['search_name']
            url = url + '&name=' + name
            ip = request.GET['search_ip']
            url = url + '&ip=' + str(ip)
            mac = request.GET['search_mac']
            url = url + '&mac=' + str(mac)

            response = requests.get(url)
            metric_data = response.json()

            do_add = False
            for j in metric_data:
                url = i.url + '/hosts/' + str(j.get('id')) + '/metrics/?format=json'
                host = requests.get(url)
                host = host.json()

                all_metrics = set()
                for metryka in host:
                    all_metrics.add(metryka['metric_id'])

                j['monitor_id'] = i.id
                j['monitor_url'] = i.url

                if cpu == 'on':
                    if 1 in all_metrics:
                        do_add = True
                elif ram == 'on':
                    if 2 in all_metrics:
                        do_add = True
                elif hdd == 'on':
                    if 3 in all_metrics:
                        do_add = True

            if do_add:
                all_metric_data.extend(metric_data)

        context = {
            'data': all_metric_data,
        }
        return render(request, 'main/search_host.html', context)

