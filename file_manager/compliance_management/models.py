from django.db import models
from accounts.models import User
from eboard_system.utils import generate_code
# Create your models here.

class ComplianceDetail(models.Model):
    compliance_name = models.CharField(max_length=200)
    compliance_score = models.IntegerField(default=0)
    compliance_start_date = models.DateTimeField(auto_now_add=False,null=True)
    compliance_end_date = models.DateTimeField(auto_now_add=False,null=True)

    def __str__(self):
        return self.compliance_name

class ChecklistDetail(models.Model):
    parent_compliance = models.ForeignKey(ComplianceDetail,on_delete=models.CASCADE,blank=True,null=True)
    check_name = models.CharField(max_length=500)
    check_description = models.CharField(max_length=700,blank=True)
    check_status = models.BooleanField(default=False)
    check_evidence_document = models.CharField(max_length=200000,blank=True,null=True)
    doc_ref = models.CharField(max_length=200,null=True,blank=True, default=generate_code())
    check_evidence = models.CharField(max_length=700,blank=True,null=True)

    def __str__(self):
        return self.check_name
