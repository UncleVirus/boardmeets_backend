from django.contrib import admin
from .models import ContractDetail,ContractStage,ContractFeedBack,ContractSignature

# Register your models here.
admin.site.register(ContractDetail)
admin.site.register(ContractStage)
admin.site.register(ContractFeedBack)
admin.site.register(ContractSignature)
