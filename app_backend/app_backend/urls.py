from django.conf.urls import url
from django.contrib import admin
from backend.views import *

urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^$', index),
        url(r'^create/$', create_acc), 
        url(r'^verify/$', verify),
        url(r'^testing/$',testing)
]