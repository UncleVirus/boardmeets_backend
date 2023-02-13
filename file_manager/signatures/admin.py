from django.contrib import admin
from .models import Signature,DocumentsToBeSigned,DocumentSignatureAnnotation

admin.site.register(Signature)
admin.site.register(DocumentsToBeSigned)
admin.site.register(DocumentSignatureAnnotation)