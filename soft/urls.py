from firmware.views import *
from django.urls import include, path
from django.views.decorators.csrf import *
from django.views.static import serve 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url , include
from firmware import views
from django.views.decorators.csrf import *
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.views import serve as serve_static


def _static_butler(request, path, **kwargs):
    return serve_static(request, path, insecure=True, **kwargs)


urlpatterns = [
    url (r'^$', csrf_exempt(home_view),name='home'),

    url(r'^loginpage',csrf_exempt(views.loginpage),name='loginpage'),

    url(r'items',views.select_items, name='items'),
    url(r'^driver',views.create_driver_element,name='driver'),
    url(r'download',csrf_exempt(views.download_driver),name="download"),
    url(r'deletedriver',views.delete_driver,name="deletedriver"),
    url(r'deleteseries',views.delete_series,name="deleteseries"),
    url(r'upload', upload_file, name='upload'),
    url(r'static/(.+)', _static_butler)
]

urlpatterns += [
    url('', include("django_prometheus.urls"))
]
