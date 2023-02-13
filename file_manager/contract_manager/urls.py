from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
# from . import views
app_name = 'contract_manager'

urlpatterns = [
    url(r'^$', views.ContractsList.as_view(), name='all_contracts'),
    url(r'^(?P<contractid>[0-9]+)/$', views.ContractUpdate.as_view(),
        name='update_delete_contract_by_id'),
    url(r'^get_contracts_to_be_signed_by_user/$',
        views.GetContractsBySignatory.as_view(), name='contract_signatory'),
    url(r'^get_contracts_to_be_approved_by_user/$',
        views.GetContractsByApprover.as_view(), name='contract_approver'),
    url(r'^percentage/(?P<percentage>[\w\-]+)/$',
        views.ContractByStatus.as_view(), name='contract_by_status'),
    url(r'^contract_stage/$', views.ContractStageUpdate.as_view(),
        name='contract_stage'),
    url(r'^contract_stage/(?P<contractid>[0-9]+)/$',
        views.ContractAllStage.as_view(), name='contract_stage'),
    url(r'^add_signeers_to_contract_document/(?P<contractid>[0-9]+)/$',
        views.CreateContractSignature.as_view(), name='contract_signature'),
    url(r'^get_signeers_of_contract_document/(?P<contractid>[0-9]+)/$',
        views.GetContractSignatureByContractId.as_view(), name='contract_signers'),
    url(r'^signing_contract_document/(?P<contractid>[0-9]+)/$',
        views.SigningContract.as_view(), name='contract_signing_document'),
    url(r'^get_contract_signature_analytics/(?P<contractid>[0-9]+)/$',
        views.GetContractSignatureAnalytics.as_view(), name='contract_signature_analytics'),
    url(r'^get_contract_feedbacks/(?P<contractid>[0-9]+)/$',
        views.GetContractFeedBacks.as_view(), name='get_contract_feedbacks'),
    url(r'^update_contract_feedbacks/(?P<feedbackId>[0-9]+)/$',
        views.ContractFeedBackUpdate.as_view(), name='update_contract_feedbacks'),
    url(r'^create_contract_feedback/(?P<contractid>[0-9]+)/$',
        views.CreateContractFeedBack.as_view(), name='create_contract_feedbacks'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
