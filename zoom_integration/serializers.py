from rest_framework import serializers
from .models import ZoomMeetings

class ZoomMeetingSerialzer(serializers.ModelSerializer):
    class Meta:
        model = ZoomMeetings
        fields = '__all__'