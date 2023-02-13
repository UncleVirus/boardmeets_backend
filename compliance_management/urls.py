from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
# from . import views
app_name = 'compliance_management'

urlpatterns = [
    url(r'^$', views.GetCompliances.as_view(), name='all_compliances'),
    url(r'^create_compliance/$', views.CreateCompliance.as_view(), name='create_compliance'),
    url(r'^create_checklist/$', views.CreateChecklist.as_view(), name='create_checklist'),
    url(r'^get_checklist/(?P<compliance_id>[0-9]+)/$', views.GetChecklistByCompliance.as_view(), name='get_checklist'),
    url(r'^mark_checklist/(?P<compliance_id>[0-9]+)/(?P<checklist_id>[0-9]+)/$', views.MarkChecklist.as_view(), name='mark_checklist'),

    url(r'^delete_compliance_by_id/(?P<compliance_id>[0-9]+)/$',views.DeleteComplianceById.as_view(),name='delete_compliance_by_id'),
    url(r'^update_compliance_by_id/(?P<compliance_id>[0-9]+)/$',views.UpdateCompliance.as_view(),name='update_compliance_by_id'),

    url(r'^delete_compliance_checklist_by_id/(?P<checklist_id>[0-9]+)/$',views.DeleteComplianceChecklistById.as_view(),name='delete_compliance_checklist_by_id'),
    url(r'^update_compliance_checklist_by_id/(?P<checklist_id>[0-9]+)/$',views.UpdateComplianceChecklist.as_view(),name='update_compliance_checklist_by_id'),

]

urlpatterns = format_suffix_patterns(urlpatterns)