from django.db import models
from accounts.models import User
from django.conf import settings
# Create your models here.

class Contact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='friends',on_delete=models.CASCADE,blank=True,null=True)
    friends = models.ManyToManyField('self',blank=True)

    def __str__(self):
        return self.user.username

class Message(models.Model):
    contact = models.ForeignKey(Contact, related_name='messages',on_delete=models.CASCADE,blank=True,null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.user.username

class Chat(models.Model):
    participants = models.ManyToManyField(Contact,related_name='chats',blank=True)
    messages = models.ManyToManyField(
        Message,related_name="chat_messages",blank=True)
    chat_title = models.CharField(max_length=200, blank=True)
    is_group = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True,null=True)
    updated_timestamp = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return "{}".format(self.pk)