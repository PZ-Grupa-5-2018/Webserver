from django.shortcuts import render
from django.shortcuts import render_to_response
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import request
import requests



def index(request):
    url = "http://www.json-generator.com/api/json/get/bTzBQZWOmq"
    response = requests.get(url)
    data = response.json()
    context = {
        'data': data,
    }
    return render(request, 'main/index.html', context)


class MonitorDataList(APIView):
    def get(self, request):
        url = "http://www.json-generator.com/api/json/get/bTzBQZWOmq"
        data = requests.get(url)
        return Response(data.json()[1])

    def post(self):
        pass
