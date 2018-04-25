from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
import requests
from .models import Monitor



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
    context = {
        'id': monitor_id,
        'url': monitor_url,
    }
    return render(request, 'main/monitors_detail.html', context)


def hosts(request, monitor_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    url = str(monitor_url) + "/hosts/"
    response = requests.get(url)
    data = response.json()
    context = {
        'hosts': data,
    }
    return render(request, 'main/hosts.html', context)


def hosts_detail(request, monitor_id, host_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    url = str(monitor_url) + "/hosts/" + str(host_id) + "/"
    response = requests.get(url)
    data = response.json()
    context = {
        'data': data,
    }
    return render(request, 'main/host_detail.html', context)


def metrics(request, monitor_id, host_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    url = str(monitor_url) + "/hosts/" + str(host_id) + "/metrics/"
    response = requests.get(url)
    data = response.json()
    context = {
        'metrics': data,
    }
    return render(request, 'main/metrics.html', context)


def metrics_detail(request, monitor_id, host_id, metric_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    url = str(monitor_url) + "/hosts/" + str(host_id) + "/metrics/" + str(metric_id)
    response = requests.get(url)
    data = response.json()
    context = {
        'data': data,
    }
    return render(request, 'main/metrics_detail.html', context)


def measurements(request, monitor_id, host_id, metric_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    url = str(monitor_url) + "/hosts/" + str(host_id) + "/metrics/" + str(metric_id) + "/measurements/"
    response = requests.get(url)
    data = response.json()
    context = {
        'measurements': data,
    }
    return render(request, 'main/measurements.html', context)


def measurements_detail(request, monitor_id, host_id, metric_id, measurement_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    url = str(monitor_url) + "/hosts/" + str(host_id) + "/metrics/" + str(metric_id) + "/measurements/" + str(measurement_id)
    response = requests.get(url)
    data = response.json()
    context = {
        'data': data,
    }
    return render(request, 'main/measurements_detail.html', context)


def login(request):
    context = {}
    return render(request, 'main/login.html', context)


def register(request):
    context = {}
    return render(request, 'main/register.html', context)


###################################
### --- TEMPORARY FOR TESTS --- ###

class HostList(APIView):
    def get(self, request):
        test_response = [{"id": 0, "ip": "123.321.34.123"}, {"id": 1, "ip": "123.321.34.123"}, {"id": 2, "ip": "123.321.34.123"}]
        return Response(test_response)

    def post(self):
        pass


class HostDetail(APIView):
    def get(self, request, pk):
        test_response = [{"id": 0, "ip": "123.321.34.123"}, {"id": 1, "ip": "123.321.34.123"}, {"id": 2, "ip": "123.321.34.123"}]
        return Response(test_response[int(pk)])

    def post(self):
        pass


class MetricList(APIView):
    def get(self, request, host_id):
        test_response = [
            [{"id": 0, "type": "ram", 'period_seconds': 60}, {"id": 1, "type": "cpu", 'period_seconds': 60}],
            [{"id": 0, "type": "ram", 'period_seconds': 160}, {"id": 1, "type": "cpu", 'period_seconds': 160}],
            [{"id": 0, "type": "ram", 'period_seconds': 60}, {"id": 1, "type": "cpu", 'period_seconds': 60}]]
        return Response(test_response[int(host_id)])

    def post(self):
        pass


class MetricDetail(APIView):
    def get(self, request, host_id, pk):
        test_response = [
            [{"id": 0, "type": "ram", 'period_seconds': 60}, {"id": 1, "type": "cpu", 'period_seconds': 60}],
            [{"id": 0, "type": "ram", 'period_seconds': 160}, {"id": 1, "type": "cpu", 'period_seconds': 160}],
            [{"id": 0, "type": "ram", 'period_seconds': 60}, {"id": 1, "type": "cpu", 'period_seconds': 60}]]
        return Response(test_response[int(host_id)][int(pk)])

    def post(self):
        pass


class MeasurementList(APIView):
    def get(self, request,host_id, metric_id):
        test_response = [
            [[{"id": 0, "value": 571, "timestamp": 123125123}, {"id": 1, "value": 571, "timestamp": 123125123}],
             [{"id": 0, "value": 571, "timestamp": 123125123}, {"id": 1, "value": 571, "timestamp": 123125123}]],
            [[{"id": 0, "value": 571, "timestamp": 123125123}, {"id": 1, "value": 571, "timestamp": 123125123}],
             [{"id": 0, "value": 571, "timestamp": 123125123}, {"id": 1, "value": 571, "timestamp": 123125123}]],
            [[{"id": 0, "value": 571, "timestamp": 123125123}, {"id": 1, "value": 571, "timestamp": 123125123}],
             [{"id": 0, "value": 571, "timestamp": 123125123}, {"id": 1, "value": 571, "timestamp": 123125123}]]
        ]
        return Response(test_response[int(host_id)][int(metric_id)])

    def post(self):
        pass

class MeasurementDetail(APIView):
    def get(self, request, host_id, metric_id, measurement_id):
        test_response = [
            [[{"id": 0, "value": 571, "timestamp": 123125123}, {"id": 1, "value": 571, "timestamp": 123125123}],
             [{"id": 0, "value": 571, "timestamp": 123125123}, {"id": 1, "value": 571, "timestamp": 123125123}]],
            [[{"id": 0, "value": 571, "timestamp": 123125123}, {"id": 1, "value": 571, "timestamp": 123125123}],
             [{"id": 0, "value": 571, "timestamp": 123125123}, {"id": 1, "value": 571, "timestamp": 123125123}]],
            [[{"id": 0, "value": 571, "timestamp": 123125123}, {"id": 1, "value": 571, "timestamp": 123125123}],
             [{"id": 0, "value": 571, "timestamp": 123125123}, {"id": 1, "value": 571, "timestamp": 123125123}]]
        ]
        return Response(test_response[int(host_id)][int(metric_id)][int(measurement_id)])

    def post(self):
        pass

### --- TEMPORARY FOR TESTS --- ###
###################################
