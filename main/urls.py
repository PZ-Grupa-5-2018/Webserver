from django.urls import path

from main.views import LoginPageView, LogoutPageView, ComplexMeasurementsView, RegisterUserView, HomePageView
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    url(r'^login/$', LoginPageView.as_view(), name='login'),
    url(r'^logout/', LogoutPageView.as_view(), name='logout'),
    url(r'^register/$', RegisterUserView.as_view(), name='register'),
    url(r'^complexMeasurements/$', ComplexMeasurementsView.as_view(), name='complex_measurements'),
    url(r'^monitors/$', views.monitors, name='monitors'),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/$', views.monitors_detail),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/download_monitor_data', views.downloadMonitorDetails),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/get_monitor_hosts', views.getMonitorHosts),
    url(r'^monitors/(?P<monitor_list>[\w\-]+)/get_last_measurements_from_monitor_list', views.getLastMeasurementsFromMonitorListView),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/get_last_measurements', views.getLastMeasurementsView),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/check_active_sensors', views.checkActiveSensors),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/hosts/(?P<host_id>[0-9]+)/$', views.hosts_detail),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/hosts/(?P<host_id>[0-9]+)/refresh_chart_measurements',
        views.refreshChartMeasurments),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/hosts/(?P<host_id>[0-9]+)/metrics/(?P<metric_id>[0-9]+)/$',
        views.metrics_detail),
    url(r'^search/$', views.search, name='search'),
    url(r'^search/search_host/', views.search_host, name='search_host'),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/hosts/(?P<host_id>[0-9]+)/add_complex_measurement',
        views.addComplexMeasurement),
]

urlpatterns = format_suffix_patterns(urlpatterns)
