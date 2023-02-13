from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import register_user_device
app_name = 'notification'

urlpatterns = [
    url(r'^create_or_update_user_device/$', register_user_device, name='create_or_update_user_device'),
]

urlpatterns = format_suffix_patterns(urlpatterns)