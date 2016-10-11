from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.tract_detail, name='tract_detail'),
    url(r'^edit/$', views.tract_cru, name='tract_update'),
]
