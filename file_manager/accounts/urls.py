from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
app_name = 'accounts'

# obtain_auth_token to obtain user token
urlpatterns = [
    url(r'^login/$',views.Login.as_view(),name='login'),
    url(r'^all_users/$',views.AllUsers.as_view(),name='all_users'),
    url(r'^user_by_id/(?P<userid>[0-9]+)/$',views.GetUserById.as_view(),name='user_by_id'),
    url(r'^update_user_by_id/(?P<userid>[0-9]+)/$',views.UpdateUser.as_view(),name='update_user_by_id'),
    url(r'^normal_update_user_by_id/(?P<userid>[0-9]+)/$',views.UpdateNormalUser.as_view(),name='normal_update_user_by_id'),
    url(r'^delete_user_by_id/(?P<userid>[0-9]+)/$',views.DeleteUserById.as_view(),name='delete_user_by_id'),
    
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    url(r'^forgot_password/$',views.ForgotPassword.as_view(),name='forgot_password'),
    url(r'^reset_password/$',views.ResetPassword.as_view(),name='forgot_password'),

    url(r'^register_user/$', views.Register.as_view(), name='register_user'),
    url(r'^verification/$',views.Two_fa_verification.as_view(),name='verification'),
    url(r'^code_resend/$',views.Code_Resend.as_view(),name='code_resend'),
    url(r'^audit_trail/$',views.Audit_Trail.as_view(),name='audit_trail'),

    url(r'^change_password/(?P<userid>[0-9]+)/$',views.ChangePassword.as_view(),name='change_password'),
    url(r'^forgot_password/$',views.ForgotPassword.as_view(),name='forgot_password'),
    url(r'^reset_password/$',views.ResetPassword.as_view(),name='reset_password'),

    url(r'^create_group/$',views.CreateGroup.as_view(),name='create_group'),
    url(r'^all_groups/$',views.GetAllGroups.as_view(),name='all_groups'),
    url(r'^update_group_by_id/(?P<groupid>[0-9]+)/$',views.UpdateGroupById.as_view(),name='update_group_by_id'),
    url(r'^delete_group_by_id/(?P<groupid>[0-9]+)/$',views.DeleteGroupById.as_view(),name='delete_group_by_id'),

    url(r'^user_by_groups/(?P<groupid>[0-9]+)/$',views.GetUserByGroups.as_view(),name='user_by_groups'),

    url(r'^create_organization_setting/$',views.CreateOrgSetting.as_view(),name='create_organization_setting'),
    url(r'^update_organization_setting/(?P<settingid>[\w\-]+)/$',views.UpdateOrgSetting.as_view(),name='update_organization_setting'),
    url(r'^delete_organization_setting/(?P<settingid>[0-9]+)/$',views.DeleteOrgSetting.as_view(),name='delete_organization_setting'),
    url(r'^get_organization_setting/(?P<orgregno>[\w\-]+)/$',views.GetOrgSettings.as_view(),name='get_organization_setting'),
    
    url(r'^create_organization_iprange/$',views.CreateIPrange.as_view(),name='create_organization_iprange'),
    url(r'^update_organization_iprange/(?P<iprangeid>[0-9]+)/$',views.UpdateIPrange.as_view(),name='update_organization_iprange'),
    url(r'^delete_organization_iprange/(?P<iprangeid>[0-9]+)/$',views.DeleteIPrange.as_view(),name='delete_organization_iprange'),
    url(r'^get_organization_iprange/(?P<orgregno>[\w\-]+)/$',views.GetOrgIPrange.as_view(),name='get_organization_iprange'),

    url(r'^department/$',views.CreateDepartment.as_view(),name='create_get_department'),
    url(r'^department/(?P<departmentid>[0-9]+)/$',views.UpdateDepartment.as_view(),name='update_delete_department'),

    
]

urlpatterns = format_suffix_patterns(urlpatterns)
