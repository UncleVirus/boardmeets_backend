from django.db import models
# from registration.models import Organization
from accounts.models import User
from django.conf import settings
from meeting_management.models import Meeting
from file_manager.models import Folder,FolderDocument
from eboard_system.utils import generate_code

# Create your models here.
class Signature(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    signature = models.CharField(max_length=200000)

    def __str__(self):
        return f"{self.user}"

class DocumentsToBeSigned(models.Model):
    signature_title = models.CharField(max_length=250, blank=True)
    open_date = models.DateTimeField(auto_now_add=False,null=True)
    close_date = models.DateTimeField(auto_now_add=False,null=True)
    description = models.CharField(max_length=250, blank=True)
    document = models.CharField(max_length=200000,blank=True,null=True)
    doc_ref = models.CharField(max_length=200,null=True,blank=True, default=generate_code())
    destination = models.ForeignKey(Folder,on_delete=models.CASCADE,blank=True,null=True)
    signers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='doc_signers', blank=True,)
    status = models.CharField(max_length=250,default='Draft')

    def __str__(self):
        return f"{self.signature_title}"


class DocumentSignatureAnnotation(models.Model):
    xfdf_string = models.TextField(default='')
    signature_document = models.ForeignKey(DocumentsToBeSigned, on_delete=models.CASCADE, blank=True, null=True)
    is_to_sign = models.BooleanField(default=False)
    signer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    signed_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        """
            model representation
        """
        return f"{self.signed_at}"