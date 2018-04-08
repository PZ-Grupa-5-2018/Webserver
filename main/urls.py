from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    path('', views.index, name='index'),
    path('monitordata', views.MonitorDataList.as_view(), name='monitordata'),
]

urlpatterns = format_suffix_patterns(urlpatterns)