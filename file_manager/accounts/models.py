from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class OrgGroup(models.Model):
    group_name = models.CharField(max_length=200)
    group_description = models.CharField(max_length=500)

    def __str__(self):
        return "{}".format(self.group_name)

class User(AbstractUser):
    email = models.EmailField('email address', unique = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    username = models.CharField(max_length=40, unique=False, default='')
    phone_no = models.CharField(max_length = 20,blank=True)
    org_reference_key = models.CharField(max_length=250, blank=True,null=True)
    twofa_status = models.BooleanField(default=False)
    org_permission = models.CharField(max_length=40,blank=True,null=True)
    profile_photo = models.CharField(max_length=20000,blank=True,null=True)
    org_groups = models.ManyToManyField(
        OrgGroup, related_name='org_group', blank=True)
    
    def __str__(self):
        return "{}".format(self.email)

class TwoFactorAuthentication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
    verification_code = models.CharField(
        "verification_code", max_length=6, blank=False)
    validated = models.BooleanField(default=False)
    expiry_time = models.CharField(max_length=100,blank=True)
    def __str__(self):
        """
        model string representation
        """
        return self.user.username

class LoginAuditTrail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True,null=True)
    ip_address = models.CharField(max_length=200,blank=True,null=True)
    login_time = models.DateTimeField(auto_now_add=False,blank=True,null=True)
    def __str__(self):
        """
        model string representation
        """
        return self.user.username

class RestToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=200)

    def __str__(self):
        return "{}".format(self.user.username)

class OrganizationSetting(models.Model):
    organization = models.CharField(max_length=200)
    ip_filtering = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.organization)

class IpAddress(models.Model):
    organization = models.CharField(max_length=200)
    ip_start = models.GenericIPAddressField()
    ip_end = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.ip_start} - {self.ip_end}"

class Department(models.Model):
    department_name = models.CharField(max_length=200,blank=True,null=True)
    department_head = models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return f"{self.department_name}"