from typing import Any, Union, List

import requests
from .models import Monitor

def getMonitorDataFromUrl(url):
    monitor_url = url
    url = str (url) + "/hosts/"
    response = requests.get (url)
    hosts = response.json ()
    hosts_data = []
    for host in hosts:
        host_url = url + str (host["id"]) + "/metrics/"
        host_response = requests.get (host_url)
        metrics = host_response.json ()
        metrics_data = []
        for metric in metrics:
            metric_url = host_url + str (metric["id"]) + "/measurements/"
            metric_response = requests.get (metric_url)
            measurements = metric_response.json ()
            single_metric_data = metric
            single_metric_data['measurements'] = measurements
            metrics_data.append (single_metric_data)
        single_host_data = host
        single_host_data['metrics'] = metrics_data
        hosts_data.append (single_host_data)
    context = {
        'monitor_url': str (monitor_url),
        'hosts': hosts_data,
    }

    return context


def getLastMeasurements(monitor_id, measurements_number):
    monitor_url = Monitor.objects.get (id=monitor_id)
    monitor_data = getMonitorDataFromUrl (monitor_url)
    all_measurements = []

    for host in monitor_data["hosts"]:
        ip = host["ip"]
        for metric in host["metrics"]:
            type = metric["type"]
            for measurement in metric["measurements"]:
                single_measurement = {}
                single_measurement["ip"] = ip
                single_measurement["type"] = type
                single_measurement["value"] = measurement["value"]
                single_measurement["timestamp"] = measurement["timestamp"]
                all_measurements.append (single_measurement)

    sorted_all_measurements = sorted (all_measurements, key=lambda k: k["timestamp"], reverse=True)
    iter = 1
    for item in sorted_all_measurements:
        item.update ({"id": iter})
        iter = iter + 1
    return sorted_all_measurements[:measurements_number]
