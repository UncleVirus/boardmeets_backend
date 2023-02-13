from django.db import models
# from registration.models import Organization

# Create your models here.

class LicenseBody(models.Model):
    license_key = models.CharField(max_length=20,blank=True)
    server_id = models.CharField(max_length=100,blank=False,null=True)
    mac_address = models.CharField(max_length=100,blank=False,null=True)
    public_n = models.CharField(max_length=1000)
    public_e = models.CharField(max_length=1000)
    signature = models.CharField(max_length=2000,blank=True)
    user_email = models.CharField(max_length=250, blank=True)
    license_type = models.CharField(max_length=250, blank=True)
    license_expiry_period = models.IntegerField(blank=True,null=True)
    number_of_users = models.IntegerField(blank=True,null=True)
    isActive = models.BooleanField(default=False)
    # organization = models.OneToOneField(Organization, on_delete=models.CASCADE,blank=True,null=True)
    organization = models.CharField(max_length=200,blank=True)

    def __str__(self):
        """
        model string representation
        """
        return self.license_key

class LicenseCurrentUsers(models.Model):
    license_key = models.ForeignKey(LicenseBody, on_delete=models.CASCADE,blank=True,null=True)
    total_number_of_users = models.IntegerField(blank=True,null=True)
    number_of_active_users = models.IntegerField(blank=True,null=True,default=0)

    def __str__(self):
        """
        model string representation
        """
        return self.license_key.license_key
