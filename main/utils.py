import requests


def getMonitorDataFromUrl(url):

    url = str(url) + "/hosts/"
    response = requests.get(url)
    hosts = response.json()
    hosts_data = []
    for host in hosts:
        host_url = url + str(host["id"]) + "/metrics/"
        host_response = requests.get(host_url)
        metrics = host_response.json()
        metrics_data = []
        for metric in metrics:
            metric_url = host_url + str(metric["id"])+ "/measurements/"
            metric_response = requests.get(metric_url)
            measurements = metric_response.json()
            single_metric_data = metric
            single_metric_data['measurements_data']=measurements
            metrics_data.append(single_metric_data)
        single_host_data=host
        single_host_data['metrics_data']=metrics_data
        hosts_data.append(single_host_data)
    context = {
        'monitor_url': url,
        'monitor_hosts': hosts_data,
    }

    return context

