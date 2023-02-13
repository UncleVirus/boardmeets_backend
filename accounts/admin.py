from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User,RestToken,TwoFactorAuthentication,LoginAuditTrail,OrgGroup,OrganizationSetting,IpAddress,Department


fields = list(UserAdmin.fieldsets)
fields[0] = (None, {'fields': ('username', 'password', 'org_reference_key','phone_no','twofa_status')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(User, UserAdmin)
admin.site.register(TwoFactorAuthentication)
admin.site.register(LoginAuditTrail)
admin.site.register(RestToken)
admin.site.register(OrgGroup)
admin.site.register(OrganizationSetting)
admin.site.register(IpAddress)
admin.site.register(Department)
