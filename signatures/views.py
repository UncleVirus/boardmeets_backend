from django.shortcuts import render
from uritemplate import partial
from eboard_system.views import AuthenticatedAPIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK)
from accounts.models import User
from file_manager.models import Folder,FolderDocument
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import SignatureSerialzier,DocuementsToBeSignedSerialzier,DocumentSignatureAnnotationSerialzier
from .models import Signature,DocumentsToBeSigned,DocumentSignatureAnnotation
from eboard_system import settings
from eboard_system.utils import send_email
from sendgrid.helpers.mail import Mail
from django.conf import settings

# Create your views here.
class CreateSignature(AuthenticatedAPIView):
    serializer_class = SignatureSerialzier
    def post(self,request,format=None):
        """
        Create a Signature
        """
        signature = request.data['signature']
        if request.data['user']:
            one_user = User.objects.get(id=request.data['user'])
        else:
            one_user = request.user

        signature = SignatureSerialzier(data = request.data)
        if signature.is_valid():
            signature.save(user=one_user)
            return Response(signature.data,status=HTTP_200_OK)
        else:
            return Response({
                "status":"Failed",
                "message":"Signature not created",
                "data":"Signature not created"
            },status=HTTP_400_BAD_REQUEST)

class UpdateSignatureById(AuthenticatedAPIView):
    serializer_class = SignatureSerialzier
    def patch(self,request,signatureid,format=None):
        """
        Update Signature by Id
        """
        one_signature = Signature.objects.filter(id=signatureid).first()
        signature = SignatureSerialzier(one_signature,data=request.data, partial=True)
        if signature.is_valid():
            signature.save()
            return Response(signature.data,status=HTTP_200_OK)
        else:
            return Response({
                "status":"Failed",
                "message":"Signature Not Updated",
                "data":"Signature Not Updated"
            },status=HTTP_400_BAD_REQUEST)

class GetAllSignatures(AuthenticatedAPIView):
    serializer_class = SignatureSerialzier
    def get(self,request,format=None):
        """
        Get all Signature
        """
        user = request.user
        if user.org_permission == 'Admin':
            all_signature = Signature.objects.all()
        else:
            all_signature = Signature.objects.filter(user=user)

        signature = SignatureSerialzier(all_signature,many=True)
        return Response(signature.data,status=HTTP_200_OK)

class GetSignatureById(AuthenticatedAPIView):
    serializer_class = SignatureSerialzier
    def get(self,request,signatureid,format=None):
        """
        Get signature by Id
        """
        one_signature = Signature.objects.filter(id=signatureid)
        signature = SignatureSerialzier(one_signature,many=True)
        return Response(signature.data,status=HTTP_200_OK)

class GetSignatureByUser(AuthenticatedAPIView):
    serializer_class = SignatureSerialzier
    def get(self,request,userid,format=None):
        """
        Get signature by user Id
        """
        one_user =  User.objects.get(id=userid)
        one_signature = Signature.objects.filter(user=one_user)
        signature = SignatureSerialzier(one_signature,many=True)
        return Response(signature.data,status=HTTP_200_OK)

class DeleteSignatureById(AuthenticatedAPIView):
    serializer_class = SignatureSerialzier
    def delete(self,request,signatureid,format=None):
        """
        Delete signature by Id
        """
        one_signature = Signature.objects.filter(id=signatureid).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)

class CreateDocumentToBeSigned(AuthenticatedAPIView):
    serializer_class = DocuementsToBeSignedSerialzier
    def post(self,request,format=None):
        """
        Create Document to be signed
        """
        destination_id = request.data['destination_folder_id']
        destination_folder = Folder.objects.get(id=destination_id)

        document_signers = list(request.data['signers'])
        doc = DocuementsToBeSignedSerialzier(data = request.data)
        if doc.is_valid():
            doc.save(signers=document_signers,destination=destination_folder)
            if 'sendEmail' in request.data.keys():
                if request.data['sendEmail']:
                    subject = "RE: Signature Required!"
                    html_message = f"<p>Click <a href=''>Sign Document</a> to access the document to be signed</p>"
                    
                    # loop via all emails
                    user_emails = []
                    for user in document_signers:
                        one_user = User.objects.get(id=user)
                        user_emails.append(one_user.email)

                    #send invitation via email
                    message = Mail(
                        from_email=settings.EMAIL_HOST_USER, 
                        to_emails=user_emails, 
                        subject=subject,
                        html_content=html_message
                        )

                    send_user_email = send_email(message)

                    return Response({
                        "status":"Ok",
                        "message":"Document created",
                        "data":"Document created",
                    },status=HTTP_200_OK)

                return Response(doc.data,status=HTTP_200_OK)
            else:
                return Response(doc.data,status=HTTP_200_OK)
        else:

            return Response({
                "status":"Failed",
                "message":"Document not created",
                "data":"Document not created"
            },status=HTTP_400_BAD_REQUEST)

class GetAllDocumentsToBesigned(AuthenticatedAPIView):
    serializer_class = DocuementsToBeSignedSerialzier
    def get(self,request,format=None):
        """
        Get all Signature
        """
        user = request.user
        if user.org_permission == 'Admin':
            all_signature = DocumentsToBeSigned.objects.all()
        else:
            all_signature = DocumentsToBeSigned.objects.filter(signers=user)

        
        if all_signature:
            signatures = DocuementsToBeSignedSerialzier(all_signature,many=True)
            return Response(signatures.data,status=HTTP_200_OK)

        return Response([],status=HTTP_200_OK)
# update signature
class UpdateDocumentToBeSignedId(AuthenticatedAPIView):
    serializer_class = DocuementsToBeSignedSerialzier
    def patch(self,request,docsignatureid,format=None):
        """
        Update Document to be signed by Id
        """
        one_docsignature = DocumentsToBeSigned.objects.get(id=docsignatureid)
        docsignature = DocuementsToBeSignedSerialzier(one_docsignature,data=request.data)
        if request.data['signers']:
            document_signers = list(request.data['signers'])
            if docsignature.is_valid():
                docsignature.save(signers=document_signers)

                if request.data['status'] == "Close":
                    if request.data['created_by']:
                        one_user = User.objects.get(id=request.data['created_by'])
                    else:
                        one_user = request.user
                    one_folder = one_docsignature.destination
                    FolderDocument.objects.create(
                        folder=one_folder,doc_file=one_docsignature.document,doc_name=one_docsignature.signature_title,created_by=one_user
                    )
                    return Response(docsignature.data,status=HTTP_200_OK)
                else:
                    return Response(docsignature.data,status=HTTP_200_OK)
            else:
                return Response({
                    "status":"Failed",
                    "message":"Signature Not Updated",
                    "data":"Signature Not Updated"
                },status=HTTP_400_BAD_REQUEST)
        else:
            if docsignature.is_valid():
                docsignature.save()
                return Response(docsignature.data,status=HTTP_200_OK)
            else:
                return Response({
                    "status":"Failed",
                    "message":"Signature Not Updated",
                    "data":"Signature Not Updated"
                },status=HTTP_400_BAD_REQUEST)

class DeleteDocumentToBeSignedById(AuthenticatedAPIView):
    serializer_class = DocuementsToBeSignedSerialzier
    def delete(self,request,docsignatureid,format=None):
        """
        Delete signature by Id
        """
        one_docsignature = DocumentsToBeSigned.objects.filter(id=docsignatureid).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)

#Signature placement on documents need to be signed
class CreateDocumenteSignaturePlacement(AuthenticatedAPIView):
    serializer_class = DocumentSignatureAnnotationSerialzier

    def post(self, request, esignatureDocId, format=None):
        """
        create Contract signature
        """
        eSignature_document = DocumentsToBeSigned.objects.get(id=esignatureDocId)
        sfdf_string = request.data['xfdfString']

        if eSignature_document is not None and sfdf_string is not None:
            docToSign_annotation_instance = DocumentSignatureAnnotation.objects.create(
                xfdf_string=sfdf_string,
                signature_document=eSignature_document,
            )

            if docToSign_annotation_instance:
                response = DocumentSignatureAnnotationSerialzier(docToSign_annotation_instance).data
                return Response(response, status=200)

            return Response({"details": "Something went wrong. "}, status=400)
        return Response({"details": "bad request. "}, status=404)

class SigningeSignatureDocument(AuthenticatedAPIView):
    serializer_class = DocumentSignatureAnnotationSerialzier

    def post(self, request, esignatureDocId, format=None):
        """
        create Contract signature
        """
        user = request.user
        eSignature_document = DocumentsToBeSigned.objects.get(id=esignatureDocId)
        sfdf_string = request.data['sfdf_string']
        exist_eSignature = DocumentSignatureAnnotation.objects.filter(signer=user).exists()

        if eSignature_document is not None and sfdf_string is not None:
            if eSignature_document.signers.filter(id=user.id).exists():
                if not exist_eSignature:

                    eSignature_instance = DocumentSignatureAnnotation.objects.create(
                        xfdf_string=sfdf_string,
                        signature_document=eSignature_document,
                        signer=user,
                        is_to_sign=True,
                    )

                    if eSignature_instance:
                        response = DocumentSignatureAnnotationSerialzier(eSignature_instance).data
                        return Response(response, status=200)
                return Response({"details": "You already signed. "}, status=400)

            return Response({"details": "You are not authorized. "}, status=400)
        return Response({"details": "bad request. "}, status=404)

class GeteSignatureDocumentAnnotation(AuthenticatedAPIView):
    serializer_class = DocumentSignatureAnnotationSerialzier

    def get(self, request, esignatureDocId, format=None):
        """
        create Contract signature
        """
        eSignature_document = DocumentsToBeSigned.objects.get(id=esignatureDocId)

        if eSignature_document is not None:
            signature_instance = DocumentSignatureAnnotation.objects.filter(signature_document=eSignature_document)
            if signature_instance:
                response = DocumentSignatureAnnotationSerialzier(signature_instance, many=True)
                return Response(response.data, status=200)

            return Response([], status=400)
        return Response({"details": "Data not found. "}, status=404)


class GeteSignatureDocumentAnalytics(AuthenticatedAPIView):
    serializer_class = DocumentSignatureAnnotationSerialzier

    def get(self, request, esignatureDocId, format=None):
        """
        create Contract signature
        """
        eSignature_document = DocumentsToBeSigned.objects.get(id=esignatureDocId)

        if eSignature_document is not None:
            eSigners_count = eSignature_document.signers.count()

            eSignature_instance = DocumentSignatureAnnotation.objects.filter(signature_document=eSignature_document, is_to_sign=True)

            if eSignature_instance:
                eSignature_count = len(eSignature_instance)
                response = DocumentSignatureAnnotationSerialzier(eSignature_instance, many=True)

                data = {'eSigners_count': eSigners_count,
                        'eSigned_count': eSignature_count, 'result': response.data}
                return Response(data, status=200)

            return Response([], status=400)
        return Response({"details": "Data not found. "}, status=404)