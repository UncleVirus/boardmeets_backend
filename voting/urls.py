from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from voting import views

app_name="voting"

urlpatterns = [
    
url(r'^create_question/$', views.CreateQuestion.as_view(), name='create_question'),
url(r'^all_questions/$', views.GetAllQuestions.as_view(), name='all_questions'),
url(r'^get_question_by_id/(?P<questionid>[0-9]+)/$',views.GetQuestionById.as_view(),name='get_question_by_id'),
url(r'^delete_question_by_id/(?P<questionid>[0-9]+)/$',views.DeleteQuestionById.as_view(),name='delete_question_by_id'),
url(r'^update_question_by_id/(?P<questionid>[0-9]+)/$',views.UpdateQuestionById.as_view(),name='update_question_by_id'),

url(r'^question_vote/$', views.QuestionVote.as_view(), name='question_vote'),
url(r'^get_question_votes_by_question/(?P<questionid>[0-9]+)/$', views.GetVoteByQuestion.as_view(), name='get_question_votes_by_question'),

url(r'^get_votes_per_question/(?P<questionid>[0-9]+)/(?P<vote>[0-9]+)/$', views.GetQuestionVotes.as_view(), name='get_yes_votes'),
]

urlpatterns = format_suffix_patterns(urlpatterns)