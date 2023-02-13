from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView 
from rest_framework import authentication, permissions
from accounts.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from eboard_system.views import AuthenticatedAPIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK)
from .models import Tasks,Comments
from meeting_management.models import Meeting
from .serializers import TaskSerialzier,CommentSerialzier
import random
from .models import Tasks,Comments

from eboard_system import settings
from sendgrid.helpers.mail import Mail
from eboard_system.utils import send_email

# Create your views here.
class CreateTask(APIView):
    serializer_class = TaskSerialzier
    def post(self,request,format=None):
        """
        Create a task
        """
        #get request.user on authenticatedapiview
        if request.data['created_by']:
            one_user = User.objects.get(id=request.data['created_by'])
        else:
            one_user = request.use

        task_assignees = list(request.data['task_assignee'])
        task_viewers = list(request.data['task_viewer'])
        
        task = TaskSerialzier(data = request.data)
        if task.is_valid():
            if request.data['meeting']:
                one_meeting =  Meeting.objects.get(id=request.data['meeting'])
                task.save(created_by=one_user,task_assignee=task_assignees,meeting=one_meeting,task_viewers=task_viewers)
                if request.data['sendEmail']:

                    subject = "RE: Task Alert!"
                    html_message = f"<p>Click <a href='http://localhost:4200/#/admin/tasks-page'>Task Link</a> to access your tasks</p>"
                    
                    # loop via all emails
                    user_emails = []
                    for user in task_assignees:
                        one_user = User.objects.get(id=user)
                        user_emails.append(one_user.email)

                    #send verification code
                    message = Mail(
                        from_email=settings.EMAIL_HOST_USER, 
                        to_emails=user_emails, 
                        subject=subject,
                        html_content=html_message
                        )

                    send_user_email = send_email(message)

                    return Response({
                        "status":"Ok",
                        "message":"Task Alert Sent",
                        "data":"Task Alert Sent",
                    },status=HTTP_200_OK)
                else:
                    return Response(task.data,status=HTTP_200_OK)
            else:
                task.save(created_by=one_user,task_assignee=task_assignees,task_viewers=task_viewers)
                if request.data['sendEmail']:

                    subject = "RE: Task Alert!"
                    html_message = f"<p>Click <a href='http://localhost:4200/#/admin/tasks-page'>Task Link</a> to access your tasks</p>"
                    
                    # loop via all emails
                    user_emails = []
                    for user in task_assignees:
                        one_user = User.objects.get(id=user)
                        user_emails.append(one_user.email)

                    #send verification code
                    message = Mail(
                        from_email=settings.EMAIL_HOST_USER, 
                        to_emails=user_emails, 
                        subject=subject,
                        html_content=html_message
                        )

                    send_user_email = send_email(message)

                    return Response({
                        "status":"Ok",
                        "message":"Task Alert Sent",
                        "data":"Task Alert Sent",
                    },status=HTTP_200_OK)
                else:
                    return Response(task.data,status=HTTP_200_OK)
        else:
            print(task.errors)
            return Response({
                "status":"Failed",
                "message":"Tasks Exists",
                "data":"Tasks Exists"
            },status=HTTP_400_BAD_REQUEST)

class UpdateTaskStatus(AuthenticatedAPIView):
    serializer_class = TaskSerialzier
    def patch(self,request,taskid,format=None):
        """
        Update task by Id
        """
        user = request.user
        one_task = Tasks.objects.get(id=taskid)
        task = TaskSerialzier(one_task,data=request.data,partial=True)
        # if request.data['task_assignee'] or request.data['task_viewer']:
        #     task_assignees = list(request.data['task_assignee'])
        #     task_viewers = list(request.data['task_viewer'])
        #     if task.is_valid():
        #         task.save(task_assignee=task_assignees,task_viewers=task_viewers)
        #         return Response(task.data,status=HTTP_200_OK)
        # else:
        #     return Response({
        #         "status":"Failed",
        #         "message":"Tasks Not Updated",
        #         "data":"Tasks Not Updated"
        #     },status=HTTP_400_BAD_REQUEST)
      
        if task.is_valid():
            task.save()
            return Response(task.data,status=HTTP_200_OK)
        else:
            return Response({
                "status":"Failed",
                "message":"Tasks Not Updated",
                "data":"Tasks Not Updated"
            },status=HTTP_400_BAD_REQUEST)

class GetAllTasks(AuthenticatedAPIView):
    serializer_class = TaskSerialzier
    def get(self,request,format=None):
        """
        Get all tasks
        """
        user = request.user
        if user.org_permission == 'Admin':
            all_tasks = Tasks.objects.all()
        else:
            all_tasks = Tasks.objects.filter(task_viewers=user)
        task = TaskSerialzier(all_tasks,many=True)
        return Response(task.data,status=HTTP_200_OK)

class GetTaskById(AuthenticatedAPIView):
    serializer_class = TaskSerialzier
    def get(self,request,taskid,format=None):
        """
        Get task by Id
        """
        one_task = Tasks.objects.filter(id=taskid)
        task = TaskSerialzier(one_task,many=True)
        return Response(task.data,status=HTTP_200_OK)

class GetTaskByAsignee(AuthenticatedAPIView):
    serializer_class = TaskSerialzier
    def get(self,request,assigneeid,format=None):
        """
        Get task by Assignee Id
        """
        one_user =  User.objects.get(id=assigneeid)
        one_task = Tasks.objects.filter(task_assignee=one_user)
        task = TaskSerialzier(one_task,many=True)
        return Response(task.data,status=HTTP_200_OK)

class GetTaskByCreator(AuthenticatedAPIView):
    serializer_class = TaskSerialzier
    def get(self,request,creatorid,format=None):
        """
        Get task by Creator Id
        """
        one_user =  User.objects.get(id=creatorid)
        one_task = Tasks.objects.filter(created_by=one_user)
        task = TaskSerialzier(one_task,many=True)
        return Response(task.data,status=HTTP_200_OK)

class GetTaskByMeeting(AuthenticatedAPIView):
    serializer_class = TaskSerialzier
    def get(self,request,meetingid,format=None):
        """
        Get task by Meeting Id
        """
        one_meeting =  Meeting.objects.get(id=meetingid)
        one_task = Tasks.objects.filter(meeting=one_meeting)
        task = TaskSerialzier(one_task,many=True)
        return Response(task.data,status=HTTP_200_OK)

class GetTaskByOrganization(AuthenticatedAPIView):
    serializer_class = TaskSerialzier
    def get(self,request,orgregno,format=None):
        """
        Get task by Organization
        """
        one_task = Tasks.objects.filter(organization=orgregno)
        task = TaskSerialzier(one_task,many=True)
        return Response(task.data,status=HTTP_200_OK)

class GetTaskByStatus(AuthenticatedAPIView):
    serializer_class = TaskSerialzier
    def get(self,request,status,format=None):
        """
        Get task by Status
        """
        user = request.user
        if user.org_permission == 'Admin':
            one_task = Tasks.objects.filter(task_status=status)
        else:
            one_task = Tasks.objects.filter(task_status=status, task_assignee=user)
        task = TaskSerialzier(one_task,many=True)
        return Response(task.data,status=HTTP_200_OK)

class GetTaskByPriority(AuthenticatedAPIView):
    serializer_class = TaskSerialzier
    def get(self,request,priority,format=None):
        """
        Get task by Priority
        """
        user = request.user
        if user.org_permission == 'Admin':
            one_task = Tasks.objects.filter(task_priority=priority)
        else:
            one_task = Tasks.objects.filter(task_priority=priority, task_assignee=user)
        
        task = TaskSerialzier(one_task,many=True)
        return Response(task.data,status=HTTP_200_OK)

class DeleteTaskById(AuthenticatedAPIView):
    serializer_class = TaskSerialzier
    def delete(self,request,taskid,format=None):
        """
        Delete task by Id
        """
        one_task = Tasks.objects.filter(id=taskid).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)

class CreateComment(AuthenticatedAPIView):
    serializer_class = CommentSerialzier
    def post(self,request,format=None):
        """
        Create a Comment
        """
        taskid = request.data['task']
        one_task = Tasks.objects.get(id=taskid)

        if request.data['commentor']:
            one_user = User.objects.get(id=request.data['commentor'])
        else:
            one_user = request.user

        comment = CommentSerialzier(data = request.data)
        if comment.is_valid():
            comment.save(task=one_task,commentor=one_user)
            return Response(comment.data,status=HTTP_200_OK)
        else:
            return Response({
                "status":"Failed",
                "message":"Comment Exists",
                "data":"Comment Exists"
            },status=HTTP_400_BAD_REQUEST)

class GetCommentByTask(AuthenticatedAPIView):
    serializer_class = CommentSerialzier
    def get(self,request,taskid,format=None):
        """
        Get comment by Task
        """
        one_task = Tasks.objects.get(id=taskid)
        one_comment = Comments.objects.filter(task=one_task)
        comment = CommentSerialzier(one_comment,many=True)
        return Response(comment.data,status=HTTP_200_OK)

class UpdateCommentById(AuthenticatedAPIView):
    serializer_class = CommentSerialzier
    def patch(self,request,commentid,format=None):
        """
        Update Comment by Id
        """
        one_comment = Comments.objects.filter(id=commentid).first()
        comment = CommentSerialzier(one_comment,data=request.data,partial=True)
        if comment.is_valid():
            comment.save()
            return Response(comment.data,status=HTTP_200_OK)
        else:
            return Response({
                "status":"Failed",
                "message":"Comment Not Updated",
                "data":"Comment Not Updated"
            },status=HTTP_400_BAD_REQUEST)

class DeleteCommentById(AuthenticatedAPIView):
    serializer_class = CommentSerialzier
    def delete(self,request,commentid,format=None):
        """
        Delete Comment by Id
        """
        one_comment = Comments.objects.filter(id=commentid).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)
