from django.contrib import admin
from .models import Survey,SurveyQuestions,SurveyResponses,SurveyRepondents

admin.site.register(Survey)
admin.site.register(SurveyQuestions)
admin.site.register(SurveyResponses)
admin.site.register(SurveyRepondents)