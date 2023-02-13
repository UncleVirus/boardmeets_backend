from django.contrib import admin
from licenses.models import LicenseBody,LicenseCurrentUsers


# Register your models here.

class LicenseBodyView(admin.ModelAdmin):
    list_display = ('license_key', 'server_id', 'mac_address','license_type','license_expiry_period','number_of_users','isActive')

admin.site.register(LicenseBody,LicenseBodyView)

class CurrentUserView(admin.ModelAdmin):
    list_display = ('license_key', 'total_number_of_users', 'number_of_active_users')
    
admin.site.register(LicenseCurrentUsers,CurrentUserView)