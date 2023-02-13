from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from system_settings.serializers import VissionstatementSerializer
from . import views

app_name = 'system-settings'

urlpatterns = [
    
    url(r'^organisation_name/$', views.OrgnameViewSet.as_view(), name='organisation_name'),
    url(r'^organisation_description/$', views.OrgdescriptionViewSet.as_view(), name='organisation_description'),
    url(r'^mission_statement/$', views.MissionstatementViewSet.as_view(), name='mission_statement'),
    url(r'^vision/$', views.VissionstatementViewSet.as_view(), name='vision'),
    url(r'^board_leaders/$', views.BoardleadersViewSet.as_view(), name='board_leaders'),
    url(r'^social_links/$', views.SociallinksViewSet.as_view(), name='social_links'), 
    url(r'^license/$', views.LicenseViewSet.as_view(), name='license')
]

urlpatterns = format_suffix_patterns(urlpatterns)