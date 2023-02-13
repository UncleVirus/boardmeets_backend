from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import generics, mixins
from .models import Folder, FolderDocument
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import FolderSerializer, FolderDocumentSerializer
from accounts.models import User
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK,HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from eboard_system.views import AuthenticatedAPIView
# Create your views here.


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_subfolders(request):
    parent = request.data.get('parent')
    data = []
    user = request.user


    if user.org_permission == 'Admin':
        folders = Folder.objects.filter(parent=parent)
    else:
        folders = Folder.objects.filter(parent=parent, created_by=user)

    if folders and len(folders) > 0:
        for folder in folders:
            data.append(FolderSerializer(folder).data)
        return Response(data, status=200)
    else:
        return Response([], status=201)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_documents_folder(request):
    folder = request.data.get('folder')
    data = []
    user = request.user
    if user:
        documents = FolderDocument.objects.filter(folder=folder)

        if documents and len(documents) > 0:
            for document in documents:
                data.append(FolderDocumentSerializer(document).data)
        else:
            return Response([], status=201)

        return Response(data, status=200)

    return Response({"detail": "Please login first"}, status=401)

class FolderList(AuthenticatedAPIView):
    serializer_class = FolderSerializer
    def get(self,request,format=None):
        """
        Get folder List
        """
        user = self.request.user
        user_permission = user.org_permission

        if user_permission == 'Admin':
            folder_l = Folder.objects.filter(parent=None)
            folder_list = FolderSerializer(folder_l,many=True)
            return Response(folder_list.data,status=HTTP_200_OK)
        
        folder_l = Folder.objects.filter(created_by=user, parent=None)
        folder_list = FolderSerializer(folder_l,many=True)
        return Response(folder_list.data,status=HTTP_200_OK)
    
    def post(self,request,format=None):
        created_user = User.objects.get(id=request.data['created_by'])
        new_folder = FolderSerializer(data = request.data)
        print(request.data)
        if 'parent' in request.data.keys():
            parent = Folder.objects.get(id=request.data['parent'])
            if new_folder.is_valid():
                new_folder.save(created_by=created_user,parent=parent)
                return Response(new_folder.data,status=HTTP_200_OK)
            else:
                print(new_folder.errors)
                return Response({
                    "status":"Failed",
                    "message":"folder Not created",
                    "data":"folder Not created"
                },status=HTTP_400_BAD_REQUEST)
        else:
            if new_folder.is_valid():
                new_folder.save(created_by=created_user)
                return Response(new_folder.data,status=HTTP_200_OK)
            else:
                print(new_folder.errors)
                return Response({
                    "status":"Failed",
                    "message":"folder Not created",
                    "data":"folder Not created"
                },status=HTTP_400_BAD_REQUEST)

class FolderDetail(APIView):
    serializer_class = FolderSerializer
    def patch(self,request,folderid,format=None):
        one_folder = Folder.objects.get(id=folderid)
        folder = FolderSerializer(one_folder,data=request.data,partial=True)
        if folder.is_valid():
            if 'permissions' in request.data.keys():
                perm = list(request.data['permissions'])
                folder.save(permissions=perm)
                return Response(folder.data,status=HTTP_200_OK)
            else:
                folder.save()
                return Response(folder.data,status=HTTP_200_OK)
        else:
            print(folder.errors)
            return Response({
                "status":"Failed",
                "message":"folder Not Updated",
                "data":"folder Not Updated"
            },status=HTTP_400_BAD_REQUEST) 

    def delete(self,request,folderid,format=None):
        """
        Delete folder by Id
        """
        Folder.objects.filter(id=folderid).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)           

class FolderPermission(APIView):
    serializer_class = FolderSerializer
    def get(self,request,userid,format=None):
        """
        Get folder permission
        """
        user = User.objects.get(id=userid)
        folders = Folder.objects.filter(permissions=user, parent=None)
        folder_list = FolderSerializer(folders,many=True)
        return Response(folder_list.data,status=HTTP_200_OK)

class FolderDocumentList(APIView):
    serializer_class = FolderDocumentSerializer
    def get(self,request,folderid,format=None):
        folder = Folder.objects.get(id=folderid)
        folder_doc_l = FolderDocument.objects.filter(folder=folder)
        folder_doc_list = FolderDocumentSerializer(folder_doc_l,many=True)
        return Response(folder_doc_list.data,status=HTTP_200_OK)

class FolderCreateDocument(APIView):
    serializer_class = FolderDocumentSerializer
    def post(self,request,format=None):
        created_user = User.objects.get(id=request.data['created_by'])
        folder = Folder.objects.get(id=request.data['folder_id'])
        new_folder_doc = FolderDocumentSerializer(data = request.data)
        if new_folder_doc.is_valid():
            new_folder_doc.save(created_by=created_user,folder=folder)
            return Response(new_folder_doc.data,status=HTTP_200_OK)
        else:
            print(new_folder_doc.errors)
            return Response({
                "status":"Failed",
                "message":"folder doc not created",
                "data":"folder  doc not created"
            },status=HTTP_400_BAD_REQUEST)

class FolderDocumentDetail(APIView):
    serializer_class = FolderDocumentSerializer
    def patch(self,request,folderdocid,format=None):
        one_folder_doc = FolderDocument.objects.get(id=folderdocid)
        folder_doc = FolderDocumentSerializer(one_folder_doc,data=request.data)
        if folder_doc.is_valid():
            folder_doc.save()
            return Response(folder_doc.data,status=HTTP_200_OK)
        else:
            print(folder_doc.errors)
            return Response({
                "status":"Failed",
                "message":"folder_doc Not Updated",
                "data":"folder_doc Not Updated"
            },status=HTTP_400_BAD_REQUEST) 

    def delete(self,request,folderdocid,format=None):
        FolderDocument.objects.filter(id=folderdocid).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)  