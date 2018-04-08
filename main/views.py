from django.shortcuts import render
from django.shortcuts import render_to_response
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import request
import requests



def index(request):
    url = "http://127.0.0.1:8000/hosts/0/metrics/0/measurements/0/"
    response = requests.get(url)
    data = response.json()
    context = {
        'url': url,
        'data': data,
    }
    return render(request, 'main/index.html', context)


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
