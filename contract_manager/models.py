from pyexpat import model
from django.db import models
from django.conf import settings
from eboard_system.utils import generate_code
# Create your models here.


class ContractDetail(models.Model):
    contract_title = models.CharField(max_length=200, blank=True, null=True)
    document = models.TextField(blank=True, null=True)
    doc_ref = models.CharField(
        max_length=200, null=True, blank=True, default=generate_code())
    approvers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='contract_approvers', blank=True,)
    signatories = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='contract_signatories', blank=True,)
    permission = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='contract_reviewers', blank=True,)
    parties = models.TextField(blank=True, null=True)
    start_date_time = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    end_date_time = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    duration = models.CharField(max_length=200)
    percentage_approval = models.IntegerField(default=0, blank=True, null=True)
    status = models.CharField(max_length=200, default="Draft")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(
        auto_now_add=True, null=False, blank=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        """
            model representation
        """
        return f"{self.contract_title}"


class ContractStage(models.Model):
    parent_contract = models.ForeignKey(
        ContractDetail, on_delete=models.CASCADE)
    action_taker = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action_done = models.CharField(max_length=200, null=True, blank=True)
    action_done_at = models.DateTimeField(
        auto_now_add=True, null=False, blank=False)

    def __str__(self):
        """
            model representation
        """
        return f"{self.parent_contract.contract_title}-{self.action_taker}- {self.action_done}"


class ContractFeedBack(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    statuses = [
        ("CONTINUE", "CONTINUE"),
        ("DISCONTINUE", "DISCONTINUE")
    ]
    status = models.CharField(
        max_length=100, choices=statuses, null=True, blank=True, default="CONTINUE")
    contract = models.ForeignKey(
        ContractDetail, on_delete=models.CASCADE, blank=False, null=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(
        auto_now_add=True, null=False, blank=False)

    def __str__(self):
        """
            model representation
        """
        return self.title


class ContractSignature(models.Model):
    xfdf_string = models.TextField(default='')
    contract = models.ForeignKey(
        ContractDetail, on_delete=models.CASCADE, blank=True, null=True)
    is_updated = models.BooleanField(default=False)
    signer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    signed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """
            model representation
        """
        return f"{self.signed_at}"
