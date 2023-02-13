from django.conf.urls import url
from . import views

app_name = 'demo'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^reg$', views.show_registration, name='reg'),
    url(r'^auth$', views.show_authentication, name='auth'),
    url(r'^meeting$', views.show_meeting, name='meeting'),
    url(r'^contractmanagement$', views.show_contract, name='contract'),
     url(r'^voting$', views.show_voting, name='voting')
]
