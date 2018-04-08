from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url


urlpatterns = [
    path('', views.index, name='index'),
    url(r'^hosts/$', views.HostList.as_view()),
    url(r'^hosts/(?P<pk>[0-9]+)/$', views.HostDetail.as_view()),
    url(r'^hosts/(?P<host_id>[0-9]+)/metrics/$', views.MetricList.as_view()),
    url(r'^hosts/(?P<host_id>[0-9]+)/metrics/(?P<pk>[0-9]+)/$', views.MetricDetail.as_view()),
    url(r'^hosts/(?P<host_id>[0-9]+)/metrics/(?P<metric_id>[0-9]+)/measurements/$', views.MeasurementList.as_view()),
    url(r'^hosts/(?P<host_id>[0-9]+)/metrics/(?P<metric_id>[0-9]+)/measurements/(?P<measurement_id>[0-9]+)/$', views.MeasurementDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)