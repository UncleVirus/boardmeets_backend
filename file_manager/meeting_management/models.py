from ast import mod
from pyexpat import model
from django.db import models
from accounts.models import User
from django.conf import settings
from eboard_system.utils import generate_code

# Create your models here.


class Meeting(models.Model):
    meeting_title = models.CharField(max_length=200)
    start_date = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=False, blank=False
    )
    end_date = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=False, blank=False
    )
    meeting_address = models.TextField(blank=True, null=True)
    invitees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='meeting_invitees', blank=True
    )
    isActive = models.BooleanField(default=True)

    def __str__(self):
        """
            model representation
        """
        return f"{self.meeting_title}"


class AgendaAction(models.Model):
    action_name = models.CharField(max_length=200, blank=True, null=True)
    person_responsible = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='agenda_responsible', blank=True
    )
    deadline = models.DateTimeField(
        auto_now=False, auto_now_add=False, null=False, blank=False
    )

    def __str__(self):
        """
            model representation
        """
        return f"{self.action_name}"


class Rsvp(models.Model):
    parent_meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    parent_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    choice = models.CharField(max_length=100)
    in_meeting_choice = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        """
            model representation
        """
        return f"{self.parent_meeting.meeting_title}-{self.parent_user.username}-{self.choice}"


class MinutesAgenda(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    discussion = models.CharField(max_length=400, blank=True, null=True)
    conclusion = models.CharField(max_length=400, blank=True, null=True)
    agenda_actions = models.ManyToManyField(
        AgendaAction, related_name="agenda_actions", blank=True)

    def __str__(self):
        """
            model representation
        """
        return f"{self.title}"


class Minutes(models.Model):
    parent_meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    invitees = models.ManyToManyField(
        Rsvp, related_name="minutes_rsvp", blank=True)
    guests = models.CharField(max_length=400, blank=True, null=True)
    agenda = models.ManyToManyField(
        MinutesAgenda, related_name="minutes_agenda", blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        """
            model representation
        """
        return f"{self.parent_meeting.meeting_title}"


class AgendaItem(models.Model):
    parent_meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    parent_item = models.ForeignKey(
        'self', blank=True, null=True, related_name='items', on_delete=models.CASCADE)
    agenda_name = models.CharField(max_length=200)
    agenda_description = models.CharField(
        max_length=200, blank=True, null=True)
    agenda_document = models.CharField(max_length=10000, blank=True, null=True)
    doc_ref = models.CharField(
        max_length=200, null=True, blank=True, default=generate_code())
    childreen = models.CharField(max_length=200, null=True, blank=True)
    permission = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='agenda_permission', blank=True
    )
    presenters = models.TextField(blank=True, null=True)
    guests = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            model representation
        """
        return f"{self.parent_meeting.meeting_title}-{self.agenda_name}"


class Annotation(models.Model):
    annotation_id = models.CharField(max_length=200)
    xfdf_string = models.TextField(default='')
    doc_ref = models.CharField(max_length=200)
    annoted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, default='')

    def __str__(self):
        """
            model representation
        """
        return f"{self.doc_ref}"
