from django.db import models
# from registration.models import Organization
from accounts.models import User
from meeting_management.models import Meeting
from django.conf import settings
from eboard_system.utils import generate_code

# Create your models here.
class Tasks(models.Model):
    # organization = models.ForeignKey(Organization, on_delete=models.CASCADE,blank=True,null=True)
    organization = models.CharField(max_length=100,blank=True,null=True)
    task_name = models.CharField(max_length=250, blank=False)
    task_description = models.CharField(max_length=250, blank=False)
    task_assignee = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='task_assignees', blank=True,)
    task_viewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='task_viewers', blank=True,)
    completion_date = models.DateTimeField(auto_now_add=False, blank=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True,related_name='created_by')
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    task_status = models.CharField(max_length=250,blank=True,null=True)
    task_priority = models.CharField(max_length=250,blank=True,null=True)
    task_document = models.CharField(max_length=200000,blank=True,null=True)
    doc_ref = models.CharField(max_length=200,null=True,blank=True, default=generate_code())
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE,blank=True,null=True)
    sendEmail = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.task_name}"

class Comments(models.Model):
    task = models.ForeignKey(Tasks,on_delete=models.CASCADE)
    comment = models.CharField(max_length=500,blank=True)
    commentor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at =  models.DateTimeField(auto_now_add=True,null=True)