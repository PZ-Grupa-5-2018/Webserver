from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import FormView, ListView
import requests

from main.forms import LoginForm, RegisterUserForm
from .models import Monitor
from .utils import getMonitorDataFromUrl
from .utils import getLastMeasurements
import json
import datetime
import time


class LoginRequiredMixin(object):
    """
   Wszystkie widoki dziedziczące po tej klasie wymagają, aby użytkownik był zalogowany
   """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class LoginPageView(FormView):
    """
   Widok służący do logowania użytkownika

   Atrybuty:
       template_name   Nazwa szablonu HTML do wczytania
       form_class      Formularz użyty w szablonie
       success_url     Strona, do której mamy być przeniesieni po pomyślnym wykonaniu funkcji post
   """
    template_name = 'main/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        # Jeśli użytkownik jest już zalogowany to przekierowujemy go na inna strone
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    # Gdy jesteśmy wylogowani, a chcemy się dostać na daną podstronę, to po zalogowaniu przekierowuje nas do niej
                    if request.POST.get('next'):
                        return HttpResponseRedirect(request.POST['next'])
                    else:
                        return HttpResponseRedirect(self.get_success_url())
            else:
                messages.error(request, '<strong>Błąd:</strong> Błędna nazwa użytkownika lub hasło.')
        return render(request, self.template_name, {'form': form})


class LogoutPageView(LoginRequiredMixin, FormView):
    """
   Widok służący do wylogowania użytkownika
   Dostęp do niego ma jedynie użytkownik zalogowany

   Atrybuty:
       template_name   Nazwa szablonu HTML do wczytania
   """
    template_name = 'main/logout.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return render(request, self.template_name)
        else:
            return HttpResponseRedirect(reverse('index'))


class ComplexMeasurementsView(LoginRequiredMixin, FormView):
    """
   Widok służący do wylogowania użytkownika
   Dostęp do niego ma jedynie użytkownik zalogowany

   Atrybuty:
       template_name   Nazwa szablonu HTML do wczytania
   """
    template_name = 'main/complex_measurements.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class RegisterUserView(FormView):
    """
    Widok służący do rejestracji nowego użytkownika (studenta)

    Atrybuty:
        template_name   Nazwa szablonu HTML do wczytania
        form_class      Formularz użyty w szablonie
        success_url     Strona, do której mamy być przeniesieni po pomyślnym wykonaniu funkcji post
    """
    template_name = 'main/register.html'
    form_class = {'user_form': RegisterUserForm}
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        user_form = self.form_class['user_form']
        return render(request, self.template_name, {'user_form': user_form})

    def post(self, request, *args, **kwargs):
        user_form = RegisterUserForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return HttpResponseRedirect(self.get_success_url())
        return render(request, self.template_name, {'user_form': user_form})


def downloadMonitorDetails(request, monitor_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    monitor_data = getMonitorDataFromUrl(monitor_url, 100)  # downloading 100 measurements
    parsed = json.loads(json.dumps(monitor_data))
    response = HttpResponse(json.dumps(parsed, indent=4, sort_keys=True), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=' + 'monitor_' + str(monitor_url) + '_data.json'

    return response


def getLastMeasurementsView(request, monitor_id):
    last_measurements = getLastMeasurements(monitor_id, 20)
    parsed = json.loads(json.dumps(last_measurements))
    response = HttpResponse(json.dumps(parsed, indent=4, sort_keys=True), content_type='application/json')
    return response


class HomePageView(View):
    """
    Strona główna

    Atrybuty:
        context                 Przekazanie danych do szablonu HTML
        template_name           Nazwa szablonu HTML do wczytania
    """
    template_name = 'main/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def monitors(request):
    monitors = Monitor.objects.all()
    context = {
        'monitors': monitors,
    }
    return render(request, 'main/monitors.html', context)


def monitors_detail(request, monitor_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    url = str(monitor_url) + "hosts/"
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


def refreshChartMeasurments(request, monitor_id, host_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    url = str(monitor_url) + "hosts/" + str(host_id) + "/metrics/"
    response = requests.get(url)
    metrics_data = response.json()

    data_chart = []
    for metric in metrics_data:
        url = str(monitor_url) + "hosts/" + str(host_id) + "/metrics/" + str(metric["id"]) + "/measurements"
        response = requests.get(url)
        measurements_data = response.json()
        measurements_data = sorted(measurements_data, key=lambda k: k['timestamp'])
        values = []
        for single_measurment in measurements_data:
            values.append({'x': time.mktime(
                datetime.datetime.strptime(single_measurment["timestamp"], "%Y-%m-%dT%H:%M:%SZ").timetuple()),
                'y': single_measurment["value"]})
        data_chart.append(dict(key=metric["type"], values=values))

    parsed = json.loads(json.dumps(data_chart))
    response = HttpResponse(json.dumps(parsed, indent=4, sort_keys=True), content_type='application/json')
    return response


def checkActiveSensors(request, monitor_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    monitor_data = getMonitorDataFromUrl(monitor_url, 1)

    sensors_measurements = []
    for host in monitor_data["hosts"]:
        host_ip = host["ip"]
        host_name = host["name"]
        host_id = host["id"]
        for metric in host["metrics"]:
            metric_type = metric["type"]
            metric_id = metric["id"]
            for measurement in metric["measurements"]:
                single_measurement = {}
                single_measurement["host_ip"] = host_ip
                single_measurement["host_name"] = host_name
                single_measurement["host_id"] = host_id
                single_measurement["metric_type"] = metric_type
                single_measurement["metric_id"] = metric_id
                single_measurement["measurement_value"] = measurement["value"]
                single_measurement["measurement_timestamp"] = measurement["timestamp"]
                sensors_measurements.append(single_measurement)

    parsed = json.loads(json.dumps(sensors_measurements))
    response = HttpResponse(json.dumps(parsed, indent=4, sort_keys=True), content_type='application/json')
    return response


def hosts_detail(request, monitor_id, host_id):
    monitor_url = Monitor.objects.get(id=monitor_id)
    url = str(monitor_url) + "hosts/" + str(host_id) + "/"
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
    url = str(monitor_url) + "hosts/" + str(host_id) + "/metrics/" + str(metric_id)
    response = requests.get(url)
    metric_data = response.json()

    url = url + "/measurements/"
    url = url + "?count=100"
    response = requests.get(url)
    measurements_data = response.json()
    context = {
        'metric_data': metric_data,
        'measurements_data': measurements_data,
    }
    return render(request, 'main/metrics_detail.html', context)


def search(request):
    context = {}
    return render(request, 'main/search.html', context)


def search_host(request):
    # 'generic' jak wyszukujemy globalnie, 'advanced' jak z urla /search
    search_type = request.GET['search_type']
    monitor = Monitor.objects.all()

    cpu = request.GET.get('CPU', 'off')
    ram = request.GET.get('RAM', 'off')
    hdd = request.GET.get('HDD', 'off')

    if search_type == 'generic':
        all_metric_data = []
        for i in monitor:
            url = i.url
            url = url + 'hosts/?format=json'
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
            url = url + 'hosts/?format=json'
            name = request.GET['search_name']
            url = url + '&name=' + name
            ip = request.GET['search_ip']
            url = url + '&ip=' + str(ip)
            mac = request.GET['search_mac']
            url = url + '&mac=' + str(mac)

            response = requests.get(url)
            metric_data = response.json()

            # do_add = False
            for j in metric_data:
                url = i.url + 'hosts/' + str(j.get('id')) + '/metrics/?format=json'
                host = requests.get(url)
                host = host.json()

                all_metrics = set()
                for metryka in host:
                    all_metrics.add(metryka['metric_id'])

                j['monitor_id'] = i.id
                j['monitor_url'] = i.url

                if cpu == 'on':
                    if 1 in all_metrics:
                        all_metric_data.append(j)
                elif ram == 'on':
                    if 2 in all_metrics:
                        all_metric_data.append(j)
                elif hdd == 'on':
                    if 3 in all_metrics:
                        all_metric_data.append(j)

        context = {
            'data': all_metric_data,
        }
        return render(request, 'main/search_host.html', context)
