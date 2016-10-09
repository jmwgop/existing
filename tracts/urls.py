from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.tract_detail, name='tract_detail'),
]
