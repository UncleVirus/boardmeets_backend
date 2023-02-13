from ast import mod
from django.db import models
from meeting_management.models import Meeting
from django.conf import settings

# Create your models here.

class ZoomMeetings(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    host_email = models.CharField(max_length=250, blank=True, null=True)
    zoom_meeting_id = models.CharField(max_length=250, blank=True, null=True)
    time_zone = models.CharField(max_length=250, blank=True, null=True)
    zoom_meeting_password = models.CharField(max_length=250, blank=True, null=True)
    zoom_topic = models.CharField(max_length=250, blank=False, null=False)
    start_time = models.DateTimeField(blank=True, null=True)
    duration = models.CharField(max_length=10, blank=True, null=True)
    start_url = models.CharField(max_length=800, blank=True, null=True)
    join_url = models.CharField(max_length=800, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.meeting.meeting_title}-{self.zoom_topic}"