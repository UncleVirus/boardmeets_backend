from django.db import models
# from registration.models import Organization
from django.contrib.auth.models import User
from django.conf import settings
from eboard_system.utils import generate_code

# Create your models here.


class Survey(models.Model):
    # organization = models.ForeignKey(Organization, on_delete=models.CASCADE,blank=True,null=True)
    organization = models.CharField(max_length=100, blank=True, null=True)
    survey_title = models.CharField(max_length=500, blank=True, null=True)
    survey_open_date = models.DateTimeField(auto_now_add=False, null=True)
    survey_close_date = models.DateTimeField(auto_now_add=False, null=True)
    survey_description = models.CharField(
        max_length=200000, blank=True, null=True)
    document = models.CharField(max_length=200000, blank=True, null=True)
    doc_ref = models.CharField(
        max_length=200, null=True, blank=True, default=generate_code())
    permissions = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='survey_permissions', blank=True,)
    survey_status = models.CharField(
        max_length=200000, blank=True, default='Draft')
    survey_created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='survey_created_by')

    def __str__(self):
        return f"{self.survey_title}"


class SurveyResponses(models.Model):
    responses = models.CharField(max_length=500, blank=True, null=True)


class SurveyQuestions(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=200, blank=True, null=True)
    question_title = models.CharField(max_length=200, blank=True, null=True)
    is_required = models.BooleanField(default=False)
    documents = models.CharField(max_length=200000, blank=True, null=True)
    doc_ref = models.CharField(
        max_length=200, null=True, blank=True, default=generate_code())
    responses = models.ManyToManyField(
        SurveyResponses, related_name='survey_responses', blank=True)
    answer = models.TextField(default='')

    def __str__(self):
        return f"{self.question_title}"


class SurveyRepondents(models.Model):
    survey_question = models.ForeignKey(
        SurveyQuestions, on_delete=models.CASCADE)
    respondent = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.TextField(default='')
    selected_responses = models.ManyToManyField(
        SurveyResponses, related_name='selected_responses', blank=True,)
