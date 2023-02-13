from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'meeting_management'

urlpatterns = [
    url(r'^create_meeting/$', views.CreateMeeting.as_view(), name='create_meeting'),

    url(r'^get_meeting_by_id/(?P<meetingid>[0-9]+)/$',
        views.GetMeetingById.as_view(), name='get_meeting_by_id'),
    url(r'^get_active_meeting/$', views.GetActiveMeeting.as_view(),
        name='get_active_meeting'),
    url(r'^get_inactive_meeting/$', views.GetInActiveMeeting.as_view(),
        name='get_inactive_meeting'),
    url(r'^get_meetings_by_range/$', views.GetMeetingByDateRange.as_view(),
        name='get_inactive_meeting'),
    url(r'^delete_meeting_by_id/(?P<meetingid>[0-9]+)/$',
        views.DeleteMeetingById.as_view(), name='delete_meeting_by_id'),
    url(r'^update_meeting_by_id/(?P<meetingid>[0-9]+)/$',
        views.UpdateMeetingById.as_view(), name='update_meeting_by_id'),
    url(r'^create_agenda_items/$', views.CreateAgendaItem.as_view(), name='create_agenda_items'),

    url(r'^get_agenda_by_id/(?P<agendaid>[0-9]+)/$',
        views.GetAgendaById.as_view(), name='get_agenda_by_id'),
    url(r'^get_agenda_by_meeting_id/(?P<meetingid>[0-9]+)/$',
        views.GetAgendaByMeetingId.as_view(), name='get_agenda_by_meeting_id'),
    url(r'^delete_agenda_by_id/(?P<agendaid>[0-9]+)/$',
        views.DeleteAgendaById.as_view(), name='delete_agenda_by_id'),
    url(r'^update_agenda_by_id/(?P<agendaid>[0-9]+)/$',
        views.UpdateAgendaById.as_view(), name='update_agenda_by_id'),

    url(r'^create_minutes/$', views.CreateMinutes.as_view(), name='create_minutes'),
    url(r'^get_minutes/(?P<meetingid>[0-9]+)/$',
        views.GetMinutesForMeeting.as_view(), name='get_minutes'),
    url(r'^update_minute_by_id/(?P<minuteid>[0-9]+)/$',
        views.UpdateMinuteById.as_view(), name='update_minute_by_id'),
    url(r'^delete_minute_by_id/(?P<minuteid>[0-9]+)/$',
        views.DeleteMinuteById.as_view(), name='delete_minute_by_id'),
    url(r'^get_minute_by_meeting/(?P<meetingid>[0-9]+)/$',
        views.GetMinuteByMeeting.as_view(), name='get_minute_by_meeting'),
    url(r'^get_minute_by_id/(?P<minuteid>[0-9]+)/$',
        views.GetMinuteById.as_view(), name='get_minute_by_id'),
    url(r'^delete_minute_by_id/(?P<minuteid>[0-9]+)/$',
        views.DeleteMinuteById.as_view(), name='delete_minute_by_id'),

    url(r'^get_analytics_by_meeting_id/(?P<meetingid>[0-9]+)/$',
        views.GetAnalyticsById.as_view(), name='get_analytics_by_meeting_id'),
    url(r'^get_user_meetings_by_id/(?P<userid>[0-9]+)/$',
        views.UserMeetingsById.as_view(), name='get_user_meetings_by_id'),

    url(r'^create_annotation/$', views.CreateAnotations.as_view(),
        name='create_annotation'),

    url(r'^get_annotations/(?P<doc_ref>[\w\-]+)/$',
        views.GetAnnotations.as_view(), name='get_annotations'),
    url(r'^update_annotations/(?P<annotation_id>[\w\-]+)/$',
        views.UpdateAnnotations.as_view(), name='update_annotations'),
    url(r'^delete_annotations/(?P<annotation_id>[\w\-]+)/$',
        views.DeleteAnnotations.as_view(), name='delete_annotations'),


    url(r'^user_rsvp_response/$', views.RsvpResponse.as_view(),
        name='user_rsvp_response'),
    url(r'^update_rsvp/(?P<meetingid>[0-9]+)/(?P<userid>[0-9]+)/$',
        views.UpdateRsvp.as_view(), name='update_rsvp'),
    url(r'^get_user_rsvp_response/(?P<meetingid>[0-9]+)/(?P<userid>[0-9]+)/$',
        views.GetRsvpResponse.as_view(), name='get_user_rsvp_response'),
    url(r'^get_rsvp_response_for_meeting/(?P<meetingid>[0-9]+)/$',
        views.GetRsvpResponseForMeeting.as_view(), name='get_rsvp_response_for_meeting'),

    url(r'^update_minute_agenda_by_id/(?P<agendaid>[0-9]+)/$',
        views.UpdateMinuteAgendaById.as_view(), name='update_minute_agenda_by_id'),
    url(r'^delete_minute_agenda_by_id/(?P<agendaid>[0-9]+)/$',
        views.DeleteMinuteAgendaById.as_view(), name='delete_minute_agenda_by_id'),

    url(r'^delete_minute_agenda_actions_by_id/(?P<actionid>[0-9]+)/$',
        views.DeleteMinuteActionById.as_view(), name='delete_minute_agenda_actions_by_id'),
    url(r'^update_minute_agenda_actions_by_id/(?P<actionid>[0-9]+)/$',
        views.UpdateActionItemById.as_view(), name='update_minute_agenda_actions_by_id'),

    url(r'^create_minutes_sub/$', views.CreateMinutesSubAgenda.as_view(),
        name='create_minutes_sub'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
