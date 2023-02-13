from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from chat import views
app_name = 'chat'

urlpatterns = [
    url(r'^$', views.ChatListView.as_view(), name=''),
    url(r'^for/(?P<username>[\w\-]+)/$', views.ChatSpecificView.as_view(), name='for'),
    url(r'^contacts/(?P<userid>[0-9]+)/$', views.UserContacts.as_view(), name='contacts'),
    url(r'^start_chat/$', views.CreateChat.as_view(), name='start_chat'),
]

urlpatterns = format_suffix_patterns(urlpatterns)