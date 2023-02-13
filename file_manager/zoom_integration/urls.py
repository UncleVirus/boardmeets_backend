from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from zoom_integration.views import GenerateMeeting,GetMeetingZoomDetails,GenerateZoomSignature
app_name = 'zoom_integration'

urlpatterns = [
    url(r'^pre_meeting/$', GenerateMeeting.as_view(), name='pre_meeting'),
    url(r'^get_zoom_meeting_details_meeting_id/(?P<meetingId>[\w\-]+)/$',
        GetMeetingZoomDetails.as_view(), name='get_zoom_meeting'),
    url(r'^generate_zoom_signature/$', GenerateZoomSignature.as_view(), name='get_zoom_signature'),
]

urlpatterns = format_suffix_patterns(urlpatterns)