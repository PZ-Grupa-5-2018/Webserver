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
    url(r'^monitors/(?P<monitor_id>[0-9]+)/get_last_measurements', views.getLastMeasurementsView),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/hosts/(?P<host_id>[0-9]+)/$', views.hosts_detail),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/hosts/(?P<host_id>[0-9]+)/refresh_chart_measurements', views.refreshChartMeasurments),
    url(r'^monitors/(?P<monitor_id>[0-9]+)/hosts/(?P<host_id>[0-9]+)/metrics/(?P<metric_id>[0-9]+)/$', views.metrics_detail),

    url(r'^search/$', views.search),
    url(r'^search/search_host/', views.search_host, name='search_host'),
]

urlpatterns = format_suffix_patterns(urlpatterns)