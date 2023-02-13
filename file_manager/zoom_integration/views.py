
from django.shortcuts import render
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK)
from rest_framework.response import Response
from eboard_system.views import AuthenticatedAPIView
from meeting_management.models import Meeting
from zoom_integration.models import ZoomMeetings
from .serializers import ZoomMeetingSerialzer
from eboard_system import settings
from datetime import datetime
from datetime import timezone
from .utils import createMeeting, generateSignature
class GenerateMeeting(AuthenticatedAPIView):
    serializer_class = ZoomMeetingSerialzer
    def post(self, request, format=None):
        meeting_id = request.data['meeting_id']
        zoom_topic = request.data['zoom_topic']
        start_time = request.data['start_time']
        duration = request.data['duration']

        main_meeting = Meeting.objects.get(id=meeting_id)
        user = request.user

        #delete old meetings to avoid duplicate
        old_meeting = ZoomMeetings.objects.filter(meeting=main_meeting).first()
        if old_meeting:
            old_meeting.delete()
        
        # create json data for post requests
        meetingdetails = {
            "topic":zoom_topic,
            "type": 2,
            "start_time": start_time,
            "duration": str(duration),
            "timezone": 'CAT',
            "agenda": "test",
            "recurrence": {
                "type": 1,
                "repeat_interval": 1
                },
            "settings": {
                "host_video": "true",
                "participant_video": "true",
                "join_before_host": "true",
                "mute_upon_entry": "False",
                "watermark": "true",
                "audio": "voip",
                "auto_recording": "cloud"
                }
            }
        response = createMeeting(meetingdetails)

        if not response:
            return Response({
                "status":"Failed",
                "message":"Zoom Meeting not Created",
            },status=400)

        zoom_instance = ZoomMeetings.objects.create(
            meeting=main_meeting,
            zoom_topic=response['topic'],
            start_time=response['start_time'],
            host_email=response['host_email'],
            zoom_meeting_id=response['id'],
            time_zone=response['timezone'],
            zoom_meeting_password=response['password'],
            duration=response['duration'],
            start_url=response['start_url'],
            join_url=response['join_url'],
            created_at=response['created_at'],
            created_by=user
        )

        if not zoom_instance:
            return Response({
                "status":"Failed",
                "message":"Something went wrong, try again.",
            },status=400)

        
        res = ZoomMeetingSerialzer(zoom_instance).data
        return Response({
            "status":"OK",
            "message":"Zoom Meeting Created",
            "data":res
        },status=HTTP_200_OK)
        
        


class GetMeetingZoomDetails(AuthenticatedAPIView):
    serializer_class = ZoomMeetingSerialzer

    def get(self, request,meetingId, format=None):
        main_meeting = Meeting.objects.get(id=meetingId)

        if main_meeting:
            zoom_details = ZoomMeetings.objects.filter(meeting=main_meeting).first()

            if zoom_details:
                data = ZoomMeetingSerialzer(zoom_details).data
                response = {
                    "message":"Data fetched successful. ",
                    "data":data
                }
                return Response(response, status=200)

            return Response({
                "message":"Data not found.",
            },status=404)
        return Response({
                "message":"Meeting not exist..",
            },status=404)
class GenerateZoomSignature(AuthenticatedAPIView):
    def post(self, request, format=None):

        data = {
        'apiKey':settings.API_KEY,
        'apiSecret':settings.API_SEC,
        'meetingNumber': request.data['meetingNumber'],
        'role':  request.data['role']
        }

        signature = generateSignature(data)
        if signature:
            return Response(signature, status=200)

        return Response({'message':"Something went wrong, try again. "}, status=400)