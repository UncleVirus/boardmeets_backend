from sendgrid.helpers.mail import Mail
from eboard_system import settings
from eboard_system.utils import send_email
from .serializers import MeetingSerializer, MinutesDocumentSerializer,AgendaItemSerializer, AnnotationSerializer, RSVPserialzier, AgendaActionSerializer, MinutesAgendaSerializer
from eboard_system.views import AuthenticatedAPIView
from rest_framework.views import APIView
from .models import Meeting, Minutes, Annotation, Rsvp, AgendaAction, MinutesAgenda,AgendaItem
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK)
from rest_framework.response import Response
from accounts.models import User
from django.conf import settings
from datetime import datetime
from notification import firebase


# Create your views here.


class CreateMeeting(AuthenticatedAPIView):
    serializer_class = MeetingSerializer

    def post(self, request, format=None):
        """
        Create a Meeting
        """
        members = list(request.data['invitees'])
        meeting = MeetingSerializer(data=request.data)
        if meeting.is_valid():
            meeting.save(invitees=members)
            if request.data['sendEmail']:

                subject = "Meeting Invitation"
                html_message = f"<p>You have been invited for a meeting on E-Board.</p>"
  
                user_emails = [] 
                for i in members:
                    user = User.objects.get(id=i)
                    user_emails.append(user.email)

                #send notification via email and on devices

                #on devices
                notify_message = {
                    "title":"Hi E-board member",
                    "data":"You are invited in the eboard meeting, please check your email"
                }
                notifiy_invitees = firebase.send_multiple_notification(members, notify_message)

                #via emal
                message = Mail(
                    from_email=settings.EMAIL_HOST_USER, 
                    to_emails=user_emails, 
                    subject=subject,
                    html_content=html_message
                    )

                send_user_email = send_email(message)
                return Response(meeting.data, status=HTTP_200_OK)

            else:
                return Response(meeting.data, status=HTTP_200_OK)
        else:
            return Response({
                "status": "Failed",
                "message": "meeting not created",
                "data": "meeting  not created"
            }, status=HTTP_400_BAD_REQUEST)


class UpdateMeetingById(AuthenticatedAPIView):
    serializer_class = MeetingSerializer

    def patch(self, request, meetingid, format=None):
        """
        Update Meeting by Id
        """
        one_meeting = Meeting.objects.filter(id=meetingid).first()
        meeting = MeetingSerializer(one_meeting, data=request.data)
        if request.data['invitees']:
            members = list(request.data['invitees'])
            if meeting.is_valid():
                meeting.save(invitees=members)
                return Response(meeting.data, status=HTTP_200_OK)
            else:
                return Response({
                    "status": "Failed",
                    "message": "meeting Not Updated",
                    "data": "meeting Not Updated"
                }, status=HTTP_400_BAD_REQUEST)
        else:
            if meeting.is_valid():
                meeting.save()
                return Response(meeting.data, status=HTTP_200_OK)
            else:
                return Response({
                    "status": "Failed",
                    "message": "meeting Not Updated",
                    "data": "meeting Not Updated"
                }, status=HTTP_400_BAD_REQUEST)


class DeleteMeetingById(AuthenticatedAPIView):
    serializer_class = MeetingSerializer

    def delete(self, request, meetingid, format=None):
        """
        Delete meeting by Id
        """
        one_meeting = Meeting.objects.filter(id=meetingid).delete()
        return Response({
            "status": "OK",
            "message": "Deleted Successfuly",
            "data": "Deleted Successfuly"
        }, status=HTTP_200_OK)


class GetMeetingById(AuthenticatedAPIView):
    serializer_class = MeetingSerializer

    def get(self, request, meetingid, format=None):
        """
        Get meeting by Id
        """
        one_meeting = Meeting.objects.filter(id=meetingid)
        meeting = MeetingSerializer(one_meeting, many=True)
        return Response(meeting.data, status=HTTP_200_OK)

class GetActiveMeeting(AuthenticatedAPIView):
    serializer_class = MeetingSerializer

    def get(self, request, format=None):
        user = request.user
        if user.org_permission == 'Admin':
            meetings = Meeting.objects.filter(end_date__gte=datetime.now())
        else:
            meetings = Meeting.objects.filter(end_date__gte=datetime.now(), invitees=user)

        active_meeting = MeetingSerializer(meetings, many=True)
        return Response(active_meeting.data, status=HTTP_200_OK)

class GetMeetingByDateRange(AuthenticatedAPIView):
    serializer_class = MeetingSerializer

    def post(self, request, format=None):
        user = request.user
        start_date = request.data['start_date']
        end_date = request.data['end_date']
        
        if user.org_permission == 'Admin':
            meetings = Meeting.objects.filter(end_date__range=[start_date, end_date])
        else:
            meetings = Meeting.objects.filter(end_date__range=[start_date, end_date], invitees=user)

        active_meeting = MeetingSerializer(meetings, many=True)
        return Response(active_meeting.data, status=HTTP_200_OK)


class GetInActiveMeeting(AuthenticatedAPIView):
    serializer_class = MeetingSerializer

    def get(self, request, format=None):
        user = request.user
        if user.org_permission == 'Admin':
            meetings = Meeting.objects.filter(end_date__lt=datetime.now())
        else:
            meetings = Meeting.objects.filter(end_date__lt=datetime.now(), invitees=user)
        inactive_meeting = MeetingSerializer(meetings, many=True)
        return Response(inactive_meeting.data, status=HTTP_200_OK)


class GetAllMeetings(AuthenticatedAPIView):
    serializer_class = MeetingSerializer

    def get(self, request, format=None):
        """
        Get all meeting
        """
        all_meetings = Meeting.objects.all()
        meeting = MeetingSerializer(all_meetings, many=True)
        return Response(meeting.data, status=HTTP_200_OK)

class CreateAgendaItem(AuthenticatedAPIView):
    serializer_class = AgendaItemSerializer

    def post(self, request, format=None):
        """
        Create a Agenda Items
        """
        meetingid = request.data['meeting_id']
        one_meeting = Meeting.objects.get(id=meetingid)

        for item in request.data['items']:
            permission = list(item['permission'])
            first_agenda_item = AgendaItem.objects.create(
                parent_meeting=one_meeting,
                agenda_name=item['agenda_name'],
                agenda_description=item['agenda_description'],
                agenda_document=item['agenda_document'],
                presenters=item['presenters'],
                guests=item['guests'],
            )
            first_agenda_item.permission.set(permission)

            if 'level_a_items' in item.keys():
                for a_item in item['level_a_items']:
                    a_permission = list(a_item['permission'])

                    second_agenda_item = AgendaItem.objects.create(
                        parent_meeting=one_meeting,
                        parent_item=first_agenda_item,
                        agenda_name=a_item['agenda_name'],
                        agenda_description=a_item['agenda_description'],
                        agenda_document=a_item['agenda_document'],
                        presenters=a_item['presenters'],
                        guests=a_item['guests'],
                    )
                    second_agenda_item.permission.set(a_permission)

                    if 'level_b_items' in a_item.keys():
                        for b_item in a_item['level_b_items']:
                            b_permission = list(b_item['permission'])

                            third_agenda_item = AgendaItem.objects.create(
                                parent_meeting=one_meeting,
                                parent_item=second_agenda_item,
                                agenda_name=b_item['agenda_name'],
                                agenda_description=b_item['agenda_description'],
                                agenda_document=b_item['agenda_document'],
                                presenters=b_item['presenters'],
                                guests=b_item['guests'],
                            )
                            third_agenda_item.permission.set(b_permission)
                          
                    
        response = AgendaItem.objects.filter(parent_meeting=one_meeting).last()
        return Response({
            "status": "OK",
            "message": "Items Added",
            "data": AgendaItemSerializer(response).data
        }, status=HTTP_200_OK)


class UpdateAgendaById(AuthenticatedAPIView):
    serializer_class = AgendaItemSerializer

    def patch(self, request, agendaid, format=None):
        """
        Update Agenda by Id
        """
        permission = list(request.data['permission'])
        request.data.pop('permission')
        one_agenda = AgendaItem.objects.filter(id=agendaid).update(**request.data)
        if one_agenda:
            item = AgendaItem.objects.get(id=agendaid)
            if permission is not None:
                item.permission.set(permission)

            return Response(AgendaItemSerializer(item).data, status=HTTP_200_OK)
        else:
            return Response({
                "status": "Failed",
                "message": "meeting Not Updated",
                "data": "meeting Not Updated"
            }, status=HTTP_400_BAD_REQUEST)


class DeleteAgendaById(AuthenticatedAPIView):
    serializer_class = AgendaItemSerializer

    def delete(self, request, agendaid, format=None):
        """
        Delete agenda by Id
        """
        one_agenda = AgendaItem.objects.filter(id=agendaid).delete()
        return Response({
            "status": "OK",
            "message": "Deleted Successfuly",
            "data": "Deleted Successfuly"
        }, status=HTTP_200_OK)


class GetAgendaById(AuthenticatedAPIView):
    serializer_class = AgendaItemSerializer

    def get(self, request, agendaid, format=None):
        """
        Get agenda by Id
        """
        one_agenda = AgendaItem.objects.filter(id=agendaid)
        agenda = AgendaItemSerializer(one_agenda, many=True)
        return Response(agenda.data, status=HTTP_200_OK)


class GetAgendaByMeetingId(AuthenticatedAPIView):
    serializer_class = AgendaItemSerializer
    def get_queryset(self):
        return 

    def get(self, request, meetingid, format=None):
        """
        Get agenda by Meeting Id
        """
        one_meeting = Meeting.objects.get(id=meetingid)
        print('=======>',one_meeting)
        if one_meeting is not None:
            main_items = AgendaItem.objects.filter(parent_meeting=one_meeting)
            agenda = AgendaItemSerializer(main_items, many=True)
        
            return Response(agenda.data, status=HTTP_200_OK)

        return Response([], status=HTTP_200_OK)


class CreateMinutes(AuthenticatedAPIView):
    serializer_class = MinutesDocumentSerializer

    def post(self, request, format=None):
        """
        Create a Minutes
        """
        meetingid = request.data['meeting_id']
        one_meeting = Meeting.objects.get(id=meetingid)
        print("got meeting>>>>>>>>>>>>..")
        print(one_meeting)

        if request.data['created_by']:
            one_user = User.objects.get(id=request.data['created_by'])
        else:
            one_user = request.user

        action_item_list = []
        meeting_agendas_list = []

        for i in request.data['agendas']:
            print("inside agendas loop")
            print(i['title'])
            for a in i['action_items']:
                print("inside action items loop")
                print(a['action_name'])
                action_items = AgendaActionSerializer(data=a)
                if action_items.is_valid():
                    person_responsible = list(a['person_responsible'])
                    n = action_items.save(
                        person_responsible=person_responsible)
                    action_item_list.append(n.id)
                else:
                    print(action_items.errors)
            agendas = MinutesAgendaSerializer(data=i)
            if agendas.is_valid():
                print("inside agendas again loop")
                x = agendas.save(agenda_actions=action_item_list)
                meeting_agendas_list.append(x)
            else:
                print(agendas.errors)
            action_item_list = []

        meeting_invitees = Rsvp.objects.filter(parent_meeting=one_meeting)
        print(meeting_invitees)

        final_minutes = Minutes.objects.create(
            parent_meeting=one_meeting, created_by=one_user, guests=request.data['guests']
        )
        final_minutes.agenda.set(meeting_agendas_list)
        final_minutes.invitees.set(list(meeting_invitees))
        meeting_agendas_list = []
        # minutes = MinutesDocumentSerializer(data = request.data)
        return Response({
            "status": "Success",
            "message": "Minutes Created",
            "data": "Minutes Created"
        }, status=HTTP_200_OK)


class GetMinutesForMeeting(AuthenticatedAPIView):
    serializer_class = MinutesDocumentSerializer

    def get(self, request, meetingid, format=None):
        """
        Get minute by Meeting Id
        """
        one_meeting = Meeting.objects.get(id=meetingid)

        one_minute = Minutes.objects.filter(parent_meeting=one_meeting)
        minute = MinutesDocumentSerializer(one_minute, many=True)
        resp = {
            "minutes_data": minute.data,
            "organization": "org"
        }
        return Response(resp, status=HTTP_200_OK)


class UpdateActionItemById(AuthenticatedAPIView):
    serializer_class = AgendaActionSerializer

    def patch(self, request, actionid, format=None):
        one_action = AgendaAction.objects.get(id=actionid)
        actions = AgendaActionSerializer(one_action, data=request.data)
        if actions.is_valid():
            person_responsible = list(request.data['person_responsible'])
            actions.save(person_responsible=person_responsible)
            return Response(actions.data, status=HTTP_200_OK)
        else:
            print(actions.errors)
            return Response({
                "status": "Error",
                "message": "Action Item Not updated",
                "data": "Action Item Not updated"
            }, status=HTTP_400_BAD_REQUEST)


class UpdateMinuteAgendaById(AuthenticatedAPIView):
    serializer_class = MinutesAgendaSerializer

    def patch(self, request, agendaid, format=None):
        one_agenda = MinutesAgenda.objects.get(id=agendaid)
        agenda = MinutesAgendaSerializer(one_agenda, data=request.data)
        if agenda.is_valid():
            agenda.save()
            return Response(agenda.data, status=HTTP_200_OK)
        else:
            print(agenda.errors)
            return Response({
                "status": "Error",
                "message": "Agenda Not updated",
                "data": "Agenda Item Not updated"
            }, status=HTTP_400_BAD_REQUEST)


class UpdateMinuteById(AuthenticatedAPIView):
    serializer_class = MinutesDocumentSerializer

    def patch(self, request, minuteid, format=None):
        one_minute = Minutes.objects.get(id=minuteid)
        minute = MinutesDocumentSerializer(one_minute, data=request.data)
        if minute.is_valid():
            minute.save()
            return Response(minute.data, status=HTTP_200_OK)
        else:
            print(minute.errors)
            return Response({
                "status": "Error",
                "message": "minute Not updated",
                "data": "minute Item Not updated"
            }, status=HTTP_400_BAD_REQUEST)


class GetMinuteByMeeting(AuthenticatedAPIView):
    serializer_class = MinutesDocumentSerializer

    def get(self, request, meetingid, format=None):
        """
        Get Minute by Meeting
        """
        one_meeting = Meeting.objects.get(id=meetingid)
        one_minutes = Minutes.objects.filter(parent_meeting=one_meeting)
        minute = MinutesDocumentSerializer(one_minutes, many=True)
        return Response(minute.data, status=HTTP_200_OK)


class GetMinuteById(AuthenticatedAPIView):
    serializer_class = MinutesDocumentSerializer

    def get(self, request, minuteid, format=None):
        """
        Get Minute by Id
        """
        one_minutes = Minutes.objects.filter(id=minuteid)
        minute = MinutesDocumentSerializer(one_minutes, many=True)
        return Response(minute.data, status=HTTP_200_OK)


class DeleteMinuteById(AuthenticatedAPIView):
    serializer_class = MinutesDocumentSerializer

    def delete(self, request, minuteid, format=None):
        """
        Delete Minute by Id
        """
        one_minutes = Minutes.objects.get(id=minuteid)
        for i in one_minutes.agenda.all():
            for a in i.agenda_actions.all():
                AgendaAction.objects.filter(id=i.id).delete()
        MinutesAgenda.objects.filter(id=i.id).delete()
        Minutes.objects.filter(id=minuteid).delete()
        return Response({
            "status": "OK",
            "message": "Deleted Successfuly",
            "data": "Deleted Successfuly"
        }, status=HTTP_200_OK)


class DeleteMinuteAgendaById(AuthenticatedAPIView):
    serializer_class = MinutesAgendaSerializer

    def delete(self, request, agendaid, format=None):
        """
        Delete Minute Agenda by Id
        """
        MinutesAgenda.objects.filter(id=agendaid).delete()
        return Response({
            "status": "OK",
            "message": "Deleted Successfuly",
            "data": "Deleted Successfuly"
        }, status=HTTP_200_OK)


class DeleteMinuteActionById(AuthenticatedAPIView):
    serializer_class = AgendaActionSerializer

    def delete(self, request, actionid, format=None):
        """
        Delete Agenda action by Id
        """
        AgendaAction.objects.filter(id=actionid).delete()
        return Response({
            "status": "OK",
            "message": "Deleted Successfuly",
            "data": "Deleted Successfuly"
        }, status=HTTP_200_OK)


class GetAnalyticsById(AuthenticatedAPIView):
    serializer_class = MeetingSerializer

    def get(self, request, meetingid, format=None):
        one_meeting = Meeting.objects.get(id=meetingid)
        invitee_count = one_meeting.invitees.count()

        meeting = Meeting.objects.get(id=meetingid)

        date_format_str = '%Y/%d/%m %H:%M:%S'
        start = meeting.start_date
        meeting_start = start.strftime(date_format_str)
        end = meeting.end_date
        meeting_end = end.strftime(date_format_str)
        start = datetime.strptime(str(meeting_start), date_format_str)
        end = datetime.strptime(str(meeting_end), date_format_str)
        # Get the interval between two datetimes as timedelta object
        meeting_length = end - start

        meeting_length_formatted = datetime.strptime(str(meeting_length), "%H:%M:%S").time()

        meeting_data = Meeting.objects.filter(id=meetingid)
        analytics = MeetingSerializer(meeting_data, many=True)

        agenda_count = AgendaItem.objects.filter(parent_meeting=one_meeting).count()

        rsvps = Rsvp.objects.filter(parent_meeting=one_meeting).count()
        if invitee_count == 0:
            views_percentage = 0
        else:
            views_percentage = (rsvps/invitee_count) * 100

        not_responded = invitee_count - rsvps
        analytics_response = {
            "meeting": analytics.data,
            "meeting_length": meeting_length_formatted,
            "Agendas": agenda_count,
            "invitees": invitee_count,
            "responded_rsvp": rsvps,
            "not_responded": not_responded,
            "views": views_percentage
        }
        return Response(analytics_response, status=HTTP_200_OK)


class UserMeetingsById(AuthenticatedAPIView):
    serializer_class = MeetingSerializer

    def get(self, request, userid, format=None):
        one_user = User.objects.get(id=userid)

        all_invitee = Meeting.objects.filter(invitees=one_user)
        invitee = MeetingSerializer(all_invitee, many=True)
        return Response(invitee.data, status=HTTP_200_OK)


class CreateAnotations(AuthenticatedAPIView):
    serializer_class = AnnotationSerializer

    def post(self, request, format=None):
        """
        Create a Annotation
        """
        user = request.user
        annotation = AnnotationSerializer(data=request.data)
        if annotation.is_valid():
            annotation.save(annoted_by=user)
            return Response(annotation.data, status=HTTP_200_OK)
        else:
            print(annotation.errors)
            return Response({
                "status": "Failed",
                "message": "Annotation not created",
                "data": "Annotation  not created"
            }, status=HTTP_400_BAD_REQUEST)


class GetAnnotations(AuthenticatedAPIView):
    serializer_class = AnnotationSerializer

    def get(self, request, doc_ref, format=None):
        """
        Get  Annotation
        """
        if doc_ref is not None:
            all_annotations = Annotation.objects.filter(doc_ref=doc_ref)
            annotation = AnnotationSerializer(all_annotations, many=True)
            if Annotation is not None:
                return Response(annotation.data, status=HTTP_200_OK)
            return Response({"details":"No annotations for this document found"}, status=404)
        return Response({"details":"Invalid document reference"}, status=400)


class UpdateAnnotations(AuthenticatedAPIView):
    serializer_class = AnnotationSerializer

    def patch(self, request, annotation_id, format=None):
        one_annotation = Annotation.objects.get(annotation_id=annotation_id)
        annotation = AnnotationSerializer(
            one_annotation, data=request.data, partial=True)
        if annotation.is_valid():
            annotation.save()
            return Response(annotation.data, status=HTTP_200_OK)
        else:
            print(annotation.errors)
            return Response({
                "status": "Error",
                "message": "annotation Not updated",
                "data": "annotation Item Not updated"
            }, status=HTTP_400_BAD_REQUEST)


class DeleteAnnotations(AuthenticatedAPIView):
    serializer_class = AnnotationSerializer

    def delete(self, request, annotation_id, format=None):
        """
        Delete  annotatio  by Id
        """
        Annotation.objects.filter(annotation_id=annotation_id).delete()
        return Response({
            "status": "OK",
            "message": "Deleted Successfuly",
            "data": "Deleted Successfuly"
        }, status=HTTP_200_OK)


class RsvpResponse(APIView):
    serializer_class = RSVPserialzier

    def post(self, request, format=None):
        one_meeting = Meeting.objects.get(id=request.data['meeting_id'])
        one_user = User.objects.get(id=request.data['user_id'])

        rsvp = RSVPserialzier(data=request.data)
        if rsvp.is_valid():
            rsvp.save(parent_meeting=one_meeting, parent_user=one_user)
            return Response(rsvp.data, status=HTTP_200_OK)
        else:
            return Response({
                "status": "Failed",
                "message": "RSVP not created",
                "data": "RSVP  not created"
            }, status=HTTP_400_BAD_REQUEST)


class UpdateRsvp(AuthenticatedAPIView):
    serializer_class = RSVPserialzier

    def patch(self, request, meetingid, userid, format=None):
        """
        Update rsvp by user
        """
        one_meeting = Meeting.objects.get(id=meetingid)
        one_user = User.objects.get(id=userid)

        one_rsvp = Rsvp.objects.filter(
            parent_meeting=one_meeting, parent_user=one_user)
        if one_rsvp:
            one_rsvp_update = Rsvp.objects.get(
                parent_meeting=one_meeting, parent_user=one_user)
            f_rsvp = RSVPserialzier(one_rsvp_update, data=request.data)

            if f_rsvp.is_valid():
                f_rsvp.save()
                return Response(f_rsvp.data, status=HTTP_200_OK)
            else:
                return Response({
                    "status": "Failed",
                    "message": "rsvp Not Updated",
                    "data": "rsvp Not Updated"
                }, status=HTTP_400_BAD_REQUEST)
        else:
            rsvp = RSVPserialzier(data=request.data)
            if rsvp.is_valid():
                rsvp.save(parent_meeting=one_meeting, parent_user=one_user)
                return Response(rsvp.data, status=HTTP_200_OK)
            else:
                return Response({
                    "status": "Failed",
                    "message": "RSVP not created",
                    "data": "RSVP  not created"
                }, status=HTTP_400_BAD_REQUEST)


class GetRsvpResponse(AuthenticatedAPIView):
    serializer_class = RSVPserialzier

    def get(self, request, meetingid, userid, format=None):
        one_meeting = Meeting.objects.get(id=meetingid)
        one_user = User.objects.get(id=userid)

        rsvp = Rsvp.objects.filter(
            parent_meeting=one_meeting, parent_user=one_user)
        rsvp_data = RSVPserialzier(rsvp, many=True)
        return Response(rsvp_data.data, status=HTTP_200_OK)


class GetRsvpResponseForMeeting(AuthenticatedAPIView):
    serializer_class = RSVPserialzier

    def get(self, request, meetingid, format=None):
        one_meeting = Meeting.objects.get(id=meetingid)

        rsvp = Rsvp.objects.filter(parent_meeting=one_meeting)
        rsvp_data = RSVPserialzier(rsvp, many=True)
        return Response(rsvp_data.data, status=HTTP_200_OK)


# subagenda creation test
class CreateMinutesSubAgenda(APIView):
    serializer_class = MinutesDocumentSerializer

    def post(self, request, format=None):
        """
        Create a Minutes Sub agenda
        """
        meetingid = request.data['meeting_id']
        one_meeting = Meeting.objects.get(id=meetingid)
        print("got meeting>>>>>>>>>>>>..")
        print(one_meeting)

        if request.data['created_by']:
            one_user = User.objects.get(id=request.data['created_by'])
        else:
            one_user = request.user

        action_item_list = []
        meeting_agendas_list = []

        for i in request.data['agendas']:
            print("inside agendas loop")
            print(i['title'])
            for a in i['action_items']:

                action_items = AgendaActionSerializer(data=a)
                if action_items.is_valid():
                    person_responsible = list(a['person_responsible'])
                else:
                    print(action_items.errors)
            if 'sub_agenda' in i.keys():
                if len(i['sub_agenda']) > 0:
                    for b in i['sub_agenda']:
                        print("sub agenda section")
                        print(b['title'])
            else:
                print("no sub agenda")
            agendas = MinutesAgendaSerializer(data=i)
            if agendas.is_valid():
                print("inside agendas again loop")
            else:
                print(agendas.errors)
            action_item_list = []

        meeting_invitees = Rsvp.objects.filter(parent_meeting=one_meeting)
        print(meeting_invitees)

        meeting_agendas_list = []
        return Response({
            "status": "Success",
            "message": "Minutes Created",
            "data": "Minutes Created"
        }, status=HTTP_200_OK)
