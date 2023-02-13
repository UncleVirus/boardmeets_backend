from django.db import models

# Create your models here.
from audioop import maxpp
from django.db import models

# Create your models here.
class Orgname(models.Model):
    orgname = models.CharField(max_length=300)

class Orgdescription(models.Model):
    orgdescription = models.CharField(max_length=1000)

class Missionstatement(models.Model):
    missionstatement = models.CharField(max_length=300)

class Vissionstatement(models.Model):
    vissionstatement = models.CharField(max_length=300)

class Boardleaders(models.Model):
   chairman = models.CharField(max_length=100)
   ceo = models.CharField(max_length=100)
   secretary = models.CharField(max_length=100)
   
class Sociallinks(models.Model):
    facebook = models.CharField(max_length=1000)
    twitter = models.CharField(max_length=1000)
    linkedin = models.CharField(max_length=1000)

class License(models.Model):
    companyname = models.CharField(max_length=500)
    serverid = models.CharField(max_length=500)
    licensekey = models.CharField(max_length=500)
    expiryperiod = models.CharField(max_length=500)












