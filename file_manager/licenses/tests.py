from django.test import TestCase

from licenses.models import LicenseBody

# Create your tests here.

class PostLicense(TestCase):
    def test_license(self):
        self.assertEquals(
            LicenseBody.objects.count(),0
        )
        response = LicenseBody.objects.create(
                license_key="license key",public_n="public n",public_e='public e',
                signature ="signature",user_email="some email",license_type="license type",
                license_expiry_date="30 days"
        )
        self.assertEquals(
            LicenseBody.objects.count(),1
        )
        print(response)
