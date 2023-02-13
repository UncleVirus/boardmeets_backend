from django.urls import path
from .views import FolderList, FolderDetail,FolderCreateDocument, FolderPermission,FolderDocumentList, FolderDocumentDetail, get_documents_folder, get_subfolders
from django.conf.urls import url

urlpatterns = [
    path('subfolders/', get_subfolders,
         name='get_subfolder'),
    path('folder/documents/', get_documents_folder,
         name='get_documents_folder'),

#     this will get all documents in a specific folder, pass the folder id
    url(r'^documents/(?P<folderid>[\w-]+)/$',FolderDocumentList.as_view(),name='documents_list'), 
#     this will be used for creating a document, post request 
    url(r'^documents/$',FolderCreateDocument.as_view(),name='documents_create'), 
#     this will be used for updating and deleting a document
    url(r'^documents_update/(?P<folderdocid>[\w-]+)/$',FolderDocumentDetail.as_view(),name='folder_documents'),

     # folder , post and get
    url(r'^folders/$',FolderList.as_view(),name='folders_list'),
     # folder patch and delete
    url(r'^folders/(?P<folderid>[\w-]+)/$',FolderDetail.as_view(),name='folders_details'),
    
    url(r'^folders_perm/(?P<userid>[0-9]+)/$',FolderPermission.as_view(),name='folders_permission_list'),
]
