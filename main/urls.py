from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^login/$', views.login),
    url(r'^register/$', views.register),
    url(r'^monitors/$', views.monitors),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/$', views.monitors_detail),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/download_monitor_data', views.downloadMonitorDetails),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/hosts/(?P<host_id>[0-9]+)/$', views.hosts_detail),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/hosts/(?P<host_id>[0-9]+)/metrics/(?P<metric_id>[0-9]+)/$', views.metrics_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)