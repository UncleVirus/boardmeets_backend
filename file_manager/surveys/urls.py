from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from surveys import views
app_name = 'surveys'

urlpatterns = [
    url(r'^create_survey/$', views.CreateSurvey.as_view(), name='create_survey'),
    url(r'^all_surveys/$', views.GetAllSurveys.as_view(), name='all_surveys'),
    url(r'^delete_survey_by_id/(?P<surveyid>[0-9]+)/$',views.DeleteSurveyById.as_view(),name='delete_survey_by_id'),
    url(r'^update_survey_by_id/(?P<surveyid>[0-9]+)/$',views.UpdateSurveyById.as_view(),name='update_survey_by_id'),

    url(r'^all_survey_questions_by_survey/(?P<surveyid>[0-9]+)/$', views.GetAllSurveyQuestionsById.as_view(), name='all_survey_questions_by_survey'),
    url(r'^create_survey_question/$', views.SurveyQuestion.as_view(), name='create_survey_question'),
    url(r'^delete_survey_question_by_id/(?P<surveyqnid>[0-9]+)/$',views.DeleteSurveyQuestionById.as_view(),name='delete_survey_question_by_id'),
    url(r'^update_survey_question_by_id/(?P<surveyqnid>[0-9]+)/$',views.UpdateSurveyQuestionById.as_view(),name='update_survey_question_by_id'),

    url(r'^delete_survey_response_by_id/(?P<respid>[0-9]+)/$',views.DeleteSurveyResponseById.as_view(),name='delete_survey_response_by_id'),
    url(r'^update_survey_response/(?P<surveyqnid>[0-9]+)/(?P<respid>[0-9]+)/$',views.UpdateSurveyResponseByQuestion.as_view(),name='update_survey_response'),
   
    url(r'^submit_question/$',views.SubmitAnswers.as_view(),name='submit_question'),

    url(r'^survey_question_analytics/(?P<questionId>[0-9]+)/$',views.SurveyQuestionAnalytics.as_view(),name='survey_question_analytics'),
    url(r'^check_if_submitted/(?P<userid>[0-9]+)/$',views.UserAnswerCheck.as_view(),name='check_if_submitted'),
    url(r'^check_if_submitted_to_question/(?P<userid>[0-9]+)/(?P<surveyid>[0-9]+)$',views.UserQuestionAnswerCheck.as_view(),name='check_if_submitted_to_question'),
]

urlpatterns = format_suffix_patterns(urlpatterns)