from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from tasks import views
app_name = 'tasks'

urlpatterns = [
    url(r'^create_task/$', views.CreateTask.as_view(), name='create_task'),
    
    url(r'^create_comment/$', views.CreateComment.as_view(), name='create_task'),
    url(r'^get_comment_by_task/(?P<taskid>[0-9]+)/$',views.GetCommentByTask.as_view(),name='get_comment_by_task'),
    
    url(r'^delete_comment_by_id/(?P<commentid>[0-9]+)/$',views.DeleteCommentById.as_view(),name='delete_comment_by_id'),
    url(r'^update_comment_by_id/(?P<commentid>[0-9]+)/$',views.UpdateCommentById.as_view(),name='update_comment_by_id'),

    url(r'^all_task/$', views.GetAllTasks.as_view(), name='all_task'),
    url(r'^get_task_by_id/(?P<taskid>[0-9]+)/$',views.GetTaskById.as_view(),name='get_task_by_id'),
    url(r'^get_task_by_assignee/(?P<assigneeid>[0-9]+)/$',views.GetTaskByAsignee.as_view(),name='get_task_by_assignee'),
    url(r'^get_task_by_creator/(?P<creatorid>[0-9]+)/$',views.GetTaskByCreator.as_view(),name='get_task_by_creator'),
    url(r'^get_task_by_meeting/(?P<meetingid>[0-9]+)/$',views.GetTaskByMeeting.as_view(),name='get_task_by_meeting'),
    url(r'^get_task_by_organization/(?P<orgregno>[\w\-]+)/$',views.GetTaskByOrganization.as_view(),name='get_task_by_organization'),

    url(r'^get_task_by_status/(?P<status>[\w\-]+)/$',views.GetTaskByStatus.as_view(),name='get_task_by_status'),
    url(r'^get_task_by_priority/(?P<priority>[\w\-]+)/$',views.GetTaskByPriority.as_view(),name='get_task_by_priority'),

    url(r'^delete_task_by_id/(?P<taskid>[0-9]+)/$',views.DeleteTaskById.as_view(),name='delete_task_by_id'),
    url(r'^update_task_by_status/(?P<taskid>[0-9]+)/$',views.UpdateTaskStatus.as_view(),name='update_task_by_id')
]

urlpatterns = format_suffix_patterns(urlpatterns)