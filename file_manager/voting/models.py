from django.db import models
from django.utils import timezone
from accounts.models import User
from django.conf import settings
from eboard_system.utils import generate_code
# # Create your models here.

class VotingQuestion(models.Model):
    title = models.CharField(max_length=250, null=False, blank=False)
    description = models.TextField('description',default=False)
    vote_start_date = models.DateTimeField(auto_now_add=True,null=True)
    vote_end_date = models.DateTimeField(auto_now_add=True,null=True)
    voters = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='voters_permissions', blank=True,)
    supporting_documents = models.CharField(max_length=200000,blank=True,null=True)
    doc_ref = models.CharField(max_length=200,null=True,blank=True, default=generate_code())
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True,related_name='voteqn_created_by')
    
    yes_votes = models.IntegerField(default=0)
    no_votes = models.IntegerField(default=0)
    abstain_votes = models.IntegerField(default=0)

    yes_percentage = models.IntegerField(default=0)
    no_percentage = models.IntegerField(default=0)
    abstain_percentage = models.IntegerField(default=0)

class Votes(models.Model):
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    voting_question = models.ForeignKey(VotingQuestion,on_delete=models.CASCADE)
    vote = models.IntegerField(default=0)
