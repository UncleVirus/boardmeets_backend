from django.shortcuts import get_object_or_404
from chat.models import Message,Chat,Contact
from accounts.models import User
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK)
from rest_framework.generics import (
    ListAPIView
)
from .models import Chat,Contact
from .serializers import ChatSerialzier,ContactSerialzier,UserSerialzier
from rest_framework.views import APIView
from eboard_system.views import AuthenticatedAPIView

class ChatListView(AuthenticatedAPIView):
    serializer_class = ChatSerialzier
    def get(self,request,format=None):
        queryset = Chat.objects.all()
        al_queryset = ChatSerialzier(queryset,many=True)
        return Response(al_queryset.data,status=HTTP_200_OK)

class ChatSpecificView(AuthenticatedAPIView):
    serializer_class = ChatSerialzier
    def get(self,request,userid,format=None):
        user = get_object_or_404(User,id=userid)
        contact = get_object_or_404(Contact,user=user)
        queryset = contact.chats.all()
        al_queryset = ChatSerialzier(queryset,many=True)
        return Response(al_queryset.data,status=HTTP_200_OK)

class UserContacts(AuthenticatedAPIView):
    serializer_class = ChatSerialzier
    def get(self,request,userid,format=None):
        user = get_object_or_404(User,id=userid)
        print(user)
        contact = get_object_or_404(Contact,user=user)
        print(contact)
        chats = Chat.objects.filter(participants=contact).order_by('-updated_timestamp')
        print(chats)
        many_chats = ChatSerialzier(chats,many=True)
        return Response(many_chats.data,status=HTTP_200_OK)

class CreateChat(AuthenticatedAPIView):
    serializer_class = ChatSerialzier
    def post(self,request,format=None):
        participants = []
        print(len(request.data['participants']))
        if len(request.data['participants'])<2:
            return Response({
                "status":"Failed",
                "message":"Participants need to be more than one",
                "data":"Participants need to be more than one"
            },status=HTTP_400_BAD_REQUEST)
        else:
            for i in request.data['participants']:
                if Contact.objects.filter(user__id=i).exists():
                    cnt = Contact.objects.get(user__id=i)
                    participants.append(cnt)
                    print("exists")
                else:
                    one_user = get_object_or_404(User,id=i)
                    print(one_user)
                    Contact.objects.create(user=one_user)
                    at = Contact.objects.get(user__id=i)
                    participants.append(at)
                    print("now exists")
            if len(participants) > 2:
                if request.data['chat_title']:
                    chats = ChatSerialzier(data = request.data)
                    user_creator = User.objects.get(id=request.data['created_by'])
                    if chats.is_valid():
                        chats.save(participants=list(participants),created_by=user_creator)
                        return Response(chats.data,status=HTTP_200_OK)
                    else:
                        print(chats.errors)
                        return Response({
                            "status":"Failed",
                            "message":"chats Exists",
                            "data":"chats Exists"
                        },status=HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        "status":"Failed",
                        "message":"Chat Title is needed",
                        "data":"Chat Title is needed"
                    },status=HTTP_400_BAD_REQUEST)
            else:
                chats = ChatSerialzier(data = request.data)
                user_creator = User.objects.get(id=request.data['created_by'])
                if chats.is_valid():
                    chats.save(participants=list(participants),created_by=user_creator)
                    return Response(chats.data,status=HTTP_200_OK)
                else:
                    print(chats.errors)
                    return Response({
                        "status":"Failed",
                        "message":"chats Exists",
                        "data":"chats Exists"
                    },status=HTTP_400_BAD_REQUEST)

def get_last_10_messages(chatid):
    try:
        chat = Chat.objects.get(id=chatid)
        return chat
    except:
        return None