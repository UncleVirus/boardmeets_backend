from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from signatures import views
app_name = 'signatures'

urlpatterns = [
    url(r'^create_signature/$', views.CreateSignature.as_view(), name='create_signature'),
    url(r'^all_signature/$', views.GetAllSignatures.as_view(), name='all_signature'),
    url(r'^get_signature_by_id/(?P<signatureid>[0-9]+)/$',views.GetSignatureById.as_view(),name='get_signature_by_id'),
    url(r'^get_signature_by_user/(?P<userid>[0-9]+)/$',views.GetSignatureByUser.as_view(),name='get_signature_by_user'),
    url(r'^delete_signature_by_id/(?P<signatureid>[0-9]+)/$',views.DeleteSignatureById.as_view(),name='delete_signature_by_id'),
    url(r'^update_signature_by_id/(?P<signatureid>[0-9]+)/$',views.UpdateSignatureById.as_view(),name='update_signature_by_id'),

    url(r'^all_document_to_be_signed_by_org/$', views.GetAllDocumentsToBesigned.as_view(), name='all_document_to_be_signed_by_org'),
    url(r'^create_document_to_be_signed/$', views.CreateDocumentToBeSigned.as_view(), name='create_document_to_be_signed'),

    url(r'^delete_to_be_signed_document_by_id/(?P<docsignatureid>[0-9]+)/$',views.DeleteDocumentToBeSignedById.as_view(),name='delete_to_be_signed_document_by_id'),
    url(r'^update_to_be_signed_document_by_id/(?P<docsignatureid>[0-9]+)/$',views.UpdateDocumentToBeSignedId.as_view(),name='update_to_be_signed_document_by_id'),

    url(r'^create_eSignature_placement/(?P<esignatureDocId>[0-9]+)/$',views.CreateDocumenteSignaturePlacement.as_view(),name='create_eSignature_placement'),
    url(r'^signing_eSignature_document/(?P<esignatureDocId>[0-9]+)/$',views.SigningeSignatureDocument.as_view(),name='signing_eSignature_document'),
    url(r'^get_eSignature_document_annotation/(?P<esignatureDocId>[0-9]+)/$',views.GeteSignatureDocumentAnnotation.as_view(),name='get_eSignature_document_annotation'),
    url(r'^get_eSignature_document_analytics/(?P<esignatureDocId>[0-9]+)/$',views.GeteSignatureDocumentAnalytics.as_view(),name='get_eSignature_document_analytics'),
]

urlpatterns = format_suffix_patterns(urlpatterns)