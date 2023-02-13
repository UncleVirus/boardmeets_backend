from django.db import models
from accounts.models import User
import uuid

from django.db.models.fields import UUIDField
from django.conf import settings
from eboard_system.utils import generate_code
# Create your models here.


class Folder(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=200, null=False, blank=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='permissions', blank=True,)
    created_at = models.DateTimeField(
        auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.name


class FolderDocument(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    doc_name = models.CharField(max_length=200, null=False, blank=False)
    doc_ref = models.CharField(max_length=200,null=True,blank=True, default=generate_code())
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE)
    types = [
        ('LINK', 'LINK'),
        ('VIDEO', 'VIDEO'),
        ('FILE', 'FILE')
    ]
    type = models.CharField(max_length=50, choices=types, default='FILE')
    doc_file = models.TextField(blank=False, null=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True, null=False, blank=False)

    def __str__(self):
        return self.doc_file
