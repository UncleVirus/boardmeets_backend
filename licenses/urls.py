from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from licenses.views import GenerateServerKey

app_name = 'licenses'

urlpatterns = [
    url(r'^generate_on_installation/$', GenerateServerKey.as_view(), name='generate_on_installation'),
]

urlpatterns = format_suffix_patterns(urlpatterns)