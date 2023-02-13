from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK,HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from eboard_system.views import AuthenticatedAPIView
from .serializers import UserSerializer,RegistrationSerializer,GroupSerializer,NormaUserUpdateSerializer,IpAddresSerialzier,IpfilteringSetting,DepartmentSerializer
from .models import User,RestToken,TwoFactorAuthentication,LoginAuditTrail,OrgGroup,OrganizationSetting,IpAddress,Department


from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password,check_password

from eboard_system.utils import send_email
from .serializers import LoginAuditTrailSerializer
import random
from django.core import mail
from django.utils.html import strip_tags
import datetime
from django.utils import timezone
from datetime import timedelta
from eboard_system import settings
from sendgrid.helpers.mail import Mail



# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class Register(APIView):
    serializer_class = RegistrationSerializer
    def post(self,request,format=None):
        
        user_data = RegistrationSerializer(data=request.data)
        if user_data.is_valid():
            data_saved = user_data.save(password = make_password(request.data['password']),org_groups=list(request.data['org_groups']))
            data_saved.username = request.data['first_name']+' '+ request.data['last_name']
            data_saved.save()
            email = request.data['email']
            board_link= '<a href="https://cosekeeboard.com/" target="_blank" rel="noopener noreferrer"> here</a>'
            board_link2= '<a href="https://help.cosekeeboard.com/" target="_blank" rel="noopener noreferrer"> here</a>'
            html_content = f'<p>Welcome to Boardmeets </p> <p> Please log in to EboardMeets using the following details</p> <p><strong>Username:</strong>{email} </p> <p><strong>Password:</strong>{request.data["password"]} </p> <p><strong>Click:</strong>{board_link} to login  </p><p> For Help and FAQs about BoardMeets </p> <p></p> <p><strong>Click:</strong>{board_link2} to read more  </p>'
            
            

            message = Mail(
                from_email=settings.EMAIL_HOST_USER, 
                to_emails=email, 
                subject='Your account has been created', 
                html_content=html_content)

            send_user_email = send_email(message)
            return Response(RegistrationSerializer(data_saved).data, status=200)
            
        else:
            print(user_data.errors)
            return Response({
                "status":"Failed",
                "message":"Registration Failed",
                "data":"Registration Failed",
            },status=HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class Login(APIView):
    serializer_class = UserSerializer
    def post(self,request,format=None):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            user_ip = x_forwarded_for.split(',')[0]
        else:
            user_ip = request.META.get('REMOTE_ADDR')
        
        logging_time = timezone.now()

        profile_data = User.objects.get(email=request.data['username'])

        LoginAuditTrail.objects.create(user=profile_data,ip_address=user_ip,login_time=logging_time)
        
        if profile_data.twofa_status == True:
            verification_code = random.randint(0000, 10000)
            try:
                auth_available = TwoFactorAuthentication.objects.get(user=profile_data)
                time_now = (datetime.datetime.now()).strftime('%d/%m/%Y %H:%M')

                if auth_available.expiry_time == time_now:
                    user_token = TwoFactorAuthentication.objects.filter(expiry_time=time_now).delete()
                    return Response({
                        "status":"Ok",
                        "message":"Verification Code expired",
                        "data":"Verification Code expired",
                    },status=HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        "status":"Ok",
                        "message":"Verification Code still exists kindly confirm it first",
                        "data":"Verification Code still exists kindly confirm it first",
                    },status=HTTP_400_BAD_REQUEST)
            except:
                current_date_and_time = datetime.datetime.now()

                hours = 1
                hours_added = datetime.timedelta(hours = hours)

                future_date_and_time = (current_date_and_time + hours_added).strftime('%d/%m/%Y %H:%M')

                try:
                    auth_available = TwoFactorAuthentication.objects.get(user=profile_data)
                    if auth_available:
                        return Response({
                            "status":"Ok",
                            "message":"Verification Code still exists kindly confirm it first",
                            "data":"Verification Code still exists kindly confirm it first",
                        },status=HTTP_400_BAD_REQUEST)
                    else:
                        TwoFactorAuthentication.objects.create(
                            user=profile_data,verification_code=verification_code,expiry_time=future_date_and_time
                        )

                        email = profile_data.email
                        #send verification code
                        message = Mail(
                            from_email=settings.EMAIL_HOST_USER, 
                            to_emails=email, 
                            subject='RE: E-Board Verification Token', 
                            html_content= '<h2>Your verification code is {}</h2>'.format(verification_code)
                            )

                        send_user_email = send_email(message)
                        if not send_user_email:
                            return Response({
                                "status":"Failed",
                                "message":"Verification Token not sent",
                                "data":"Verification Token not sent",
                            },status=HTTP_400_BAD_REQUEST)

                        return Response({
                            "status":"Ok",
                            "message":"Verification Sent",
                            "data":"Verification Sent",
                        },status=HTTP_201_CREATED)

                except:
                        TwoFactorAuthentication.objects.create(
                            user=profile_data,verification_code=verification_code,expiry_time=future_date_and_time
                        )

                        message = Mail(
                            from_email=settings.EMAIL_HOST_USER, 
                            to_emails=email, 
                            subject='RE: E-Board Verification Token', 
                            html_content= '<h2>Your verification code is {}</h2>'.format(verification_code)
                            )
                        send_user_email = send_email(message)
                        if not send_user_email:
                            return Response({
                                "status":"Failed",
                                "message":"Verification Token not sent",
                                "data":"Verification Token",
                            },status=HTTP_400_BAD_REQUEST)

                        return Response({
                            "status":"Ok",
                            "message":"Verification Sent",
                            "data":"Verification Sent",
                        },status=HTTP_201_CREATED)

        else:
            username = request.data['username']
            password = request.data['password']

            if username is None or password is None:
                return Response({'error': 'Please provide both username and password'},
                                status=HTTP_400_BAD_REQUEST)
            user = authenticate(username=username, password=password)
            if not user:
                return Response({'error': 'Invalid Credentials'},
                                status=HTTP_404_NOT_FOUND)
            else:
                token, _ = Token.objects.get_or_create(user=user)
                #token_expire_handler will check, if the token is expired it will generate new one
                is_expired, token = token_expire_handler(token)
                # if is_expired:
                #     raise exceptions.AuthenticationFailed("The Token is expired") 
                one_user = User.objects.filter(id=token.user_id)
                print("user")
                one_by_user = User.objects.get(id=token.user_id)
                print(one_by_user)
                
                only_user = UserSerializer(one_user,many=True)
            
                return Response({'user':only_user.data,'expires_in': expires_in(token),'token': token.key},
                                status=HTTP_200_OK)
                            

class Logout(AuthenticatedAPIView):
    def post(self,request,format=None):
        request.user.auth_token.delete()
        logout(request)
        return Response({"message":"Logged Out"})

class ForgotPassword(APIView):
    def post(self,request,format=None):
        try:
            user = User.objects.get(email=request.data['email'])
            print(user)

            subject = "E-BOARD RESET PASSWORD"
            reset_link = '127.0.0.1:4200/forgot-password-page/'
            reset_code = random.randint(0000, 10000)

            RestToken.objects.create(user=user,token=reset_code)

            html_message = f"<p>Reset Link, <a href= '{reset_link}'>Here</a>, Use this code to reset your password {reset_code}</p>"
            email = user.email
            message = Mail(
                from_email=settings.EMAIL_HOST_USER, 
                to_emails=email, 
                subject=subject,
                html_content= html_message
                )
            send_user_email = send_email(message)
            print('email',send_email)
            if not send_user_email:
                return Response({
                    "status":"Failed",
                    "message":"Verification Token not sent",
                    "data":"Verification Token",
                },status=HTTP_400_BAD_REQUEST)

            return Response({
                "status":"Ok",
                "message":"Rest link Sent",
                "data":"Reset Link Sent",
            },status=HTTP_201_CREATED)

        except:
            return Response({
                "status":"Failed",
                "message":"Email does not exist",
                "data":"Email does not exist",
            },status=HTTP_400_BAD_REQUEST)

class ResetPassword(APIView):
    def post(self,request,format=None):
        user = User.objects.get(email=request.data['email'])
        print(user)

        reset_value = RestToken.objects.filter(user=user,token=request.data['reset_code'])
        if reset_value:
            new_password = request.data['new_password']
            User.objects.filter(id=user.id).update(password=make_password(new_password))
            reset_value.delete()
            return Response({
                "status":"Ok",
                "message":"Password reset succesful",
                "data":"Password reset succesful",
            },status=HTTP_200_OK)
        else:
            return Response({
                "status":"Ok",
                "message":"Password reset failed",
                "data":"Password reset failed",
            },status=HTTP_400_BAD_REQUEST)

class ChangePassword(AuthenticatedAPIView):
    serializer_class = UserSerializer
    def patch(self,request,userid,format=None):
        user = User.objects.get(id=userid)
        old_password = user.password
        confirm_old_password = request.data['old_password']
        if check_password(confirm_old_password,old_password):
            new_password = make_password(request.data['new_password'])
            User.objects.filter(id=userid).update(password=new_password)
            return Response({
                "status":"Ok",
                "message":"Password reset succesful",
                "data":"Password reset succesful",
            },status=HTTP_200_OK)
        else:
            return Response({
                "status":"Ok",
                "message":"Password reset Failed",
                "data":"Password reset Failed",
            },status=HTTP_400_BAD_REQUEST)

class AllUsers(AuthenticatedAPIView):
    serializer_class = UserSerializer
    def get(self,request,format=None):
        users = User.objects.all()
        all_users = UserSerializer(users,many=True)
        return Response(all_users.data,status=HTTP_200_OK)

class GetUserById(AuthenticatedAPIView):
    serializer_class = UserSerializer
    def get(self,request,userid,format=None):
        user = User.objects.filter(id=userid)
        one_users = UserSerializer(user,many=True)
        return Response(one_users.data,status=HTTP_200_OK)

#this is admin
class UpdateUser(AuthenticatedAPIView):
    serializer_class = UserSerializer
    def patch(self,request,userid,format=None):
        one_user=User.objects.get(id=userid)
        print(one_user)
        request.data['password'] = one_user.password
        user_update = UserSerializer(one_user,data=request.data)
        if user_update.is_valid():
            user_update.save(org_groups=list(request.data['org_groups']))
            return Response(user_update.data,status=HTTP_200_OK)
        else:
            print(user_update.errors)
            return Response({
                "status":"Failed",
                "message":"User Not Updated",
                "data":"User Not Updated"
            },status=HTTP_400_BAD_REQUEST)

#this is normal user
class UpdateNormalUser(AuthenticatedAPIView):
    serializer_class = NormaUserUpdateSerializer
    def patch(self,request,userid,format=None):
        one_user=User.objects.get(id=userid)
        print(one_user)
        user_update = NormaUserUpdateSerializer(one_user,data=request.data)
        if user_update.is_valid():
            user_update.save()
            return Response(user_update.data,status=HTTP_200_OK)
        else:
            print(user_update.errors)
            return Response({
                "status":"Failed",
                "message":"User Not Updated",
                "data":"User Not Updated"
            },status=HTTP_400_BAD_REQUEST)

class DeleteUserById(AuthenticatedAPIView):
    serializer_class = UserSerializer
    def delete(self,request,userid,format=None):
        """
        Delete User by Id
        """
        User.objects.get(id=userid).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)

class Two_fa_verification(APIView):
    def post(self,request,format=None):
        username = request.data['username']
        password = request.data['password']
        auth_code = request.data['auth_code']

        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        else:
            try:
                token, _ = Token.objects.get_or_create(user=user)
                is_expired, token = token_expire_handler(token)
                # if is_expired:
                #     raise exceptions.AuthenticationFailed("The Token is expired") 
                one_user = User.objects.filter(id=token.user_id)
                print("user")
                one_by_user = User.objects.get(id=token.user_id)
                print(one_by_user)
                
                only_user = UserSerializer(one_user,many=True)
                twofa_token = TwoFactorAuthentication.objects.filter(verification_code=auth_code,user=one_by_user)
                print("Geeting Toke>>>>>")
                print(twofa_token)
                if twofa_token:
                    print(" Token found now Deleting>>>>>")
                    # user_verify = TwoFactorAuthentication.objects.filter(verification_code=auth_code,user=one_by_user).update(validated=True)
                    user_token = TwoFactorAuthentication.objects.filter(verification_code = auth_code).delete()

                    return Response({'user':only_user.data,'expires_in': expires_in(token),'token': token.key},
                                    status=HTTP_200_OK)
                else:
                    return Response({"status":"false","data":"Invalid Code","message":"Inavalid code"})
            except:
                return Response({"status":"false","data":"Invalid Code","message":"Inavalid code"})

class Code_Resend(APIView):
    def post(self,request,format=None):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)

            try:
                token = TwoFactorAuthentication.objects.get(user=user)
                print("Geeting Toke>>>>>")
                if token:

                    subject = "RE: E-Board Verification Token"
                    html_message = f"<p>Verification Token, {token.verification_code}</p>"

                    message = Mail(
                    from_email=settings.EMAIL_HOST_USER, 
                    to_emails=email, 
                    subject=subject,
                    html_content= html_message
                    )

                    send_user_email = send_email(message)
                    if not send_user_email:
                        return Response({
                            "status":"Failed",
                            "message":"Verification Token not sent",
                            "data":"Verification Token",
                        },status=HTTP_400_BAD_REQUEST)
                else:
                    return Response({"status":"false","data":"Invalid Email/No Code","message":"Invalid Email/No Code"})
            except:
                return Response({"status":"false","data":"Invalid Email/No Code","message":"Invalid Email/No Code"})
        except:
            return Response({"status":"false","data":"Invalid Email","message":"Invalid Email"})

class Audit_Trail(AuthenticatedAPIView):
    serializer_class = LoginAuditTrailSerializer
    def get(self,request,format=None):
        """
        Get all Login Trail
        """
        all_trail = LoginAuditTrail.objects.all()
        print(all_trail)
        trail = LoginAuditTrailSerializer(all_trail,many=True)
        return Response(trail.data,status=HTTP_200_OK)

#this return left time
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    return left_time

# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)

def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user = token.user)
    return is_expired, token

class CreateGroup(AuthenticatedAPIView):
    serializer_class = GroupSerializer
    def post(self,request,format=None):
        """
        Create a Group
        """
        group = GroupSerializer(data = request.data)
        if group.is_valid():
            group.save()
            return Response(group.data,status=HTTP_200_OK)
        else:
            print(group.errors)
            return Response({
                "status":"Failed",
                "message":"group not created",
                "data":"surgroupvey not created"
            },status=HTTP_400_BAD_REQUEST)

class GetAllGroups(AuthenticatedAPIView):
    serializer_class = GroupSerializer
    def get(self,request,format=None):
        """
        Get all Groups 
        """
        all_groups = OrgGroup.objects.all()
        groups= GroupSerializer(all_groups,many=True)
        return Response(groups.data,status=HTTP_200_OK)

class GetUserByGroups(AuthenticatedAPIView):
    serializer_class = GroupSerializer
    def get_queryset(self):
        return

    def get(self,request,groupid,format=None):
        """
        Get all users by groups 
        """
        group = OrgGroup.objects.get(id=groupid)
        all_users = User.objects.filter(org_groups=group)
        users= UserSerializer(all_users,many=True)
        return Response(users.data,status=HTTP_200_OK)

class UpdateGroupById(AuthenticatedAPIView):
    serializer_class = GroupSerializer
    def patch(self,request,groupid,format=None):
        """
        Update Group by Id
        """
        one_group = OrgGroup.objects.get(id=groupid)
        group = GroupSerializer(one_group,data=request.data)
        if group.is_valid():
            group.save()
            return Response(group.data,status=HTTP_200_OK)
        else:
            print(group.errors)
            return Response({
                "status":"Failed",
                "message":"group Not Updated",
                "data":"group Not Updated"
            },status=HTTP_400_BAD_REQUEST)

class DeleteGroupById(AuthenticatedAPIView):
    serializer_class = GroupSerializer
    def delete(self,request,groupid,format=None):
        """
        Delete Group by Id
        """
        OrgGroup.objects.filter(id=groupid).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)

class CreateOrgSetting(AuthenticatedAPIView):
    serializer_class = IpfilteringSetting
    def post(self,request,format=None):
        org_setting = IpfilteringSetting(data=request.data)
        if org_setting.is_valid():
            org_setting.save()
            return Response(org_setting.data,status=HTTP_200_OK)
        else:
            print(org_setting.errors)
            return Response({
                "status":"Failed",
                "message":"Org Setting not created",
                "data":"Org Setting not created"
            },status=HTTP_400_BAD_REQUEST)

class UpdateOrgSetting(AuthenticatedAPIView):
    serializer_class = IpfilteringSetting
    def patch(self,request,settingid,format=None):
        one_org = OrganizationSetting.objects.get(id=settingid)
        org_setting = IpfilteringSetting(one_org,data=request.data)
        if org_setting.is_valid():
            org_setting.save()
            return Response(org_setting.data,status=HTTP_200_OK)
        else:
            print(org_setting.errors)
            return Response({
                "status":"Failed",
                "message":"Org Setting not updated",
                "data":"Org Setting not updated"
            },status=HTTP_400_BAD_REQUEST)

class DeleteOrgSetting(AuthenticatedAPIView):
    serializer_class = IpfilteringSetting
    def delete(self,request,settingid,format=None):
        OrganizationSetting.objects.filter(id=settingid).delete()
        return Response({
            "status":"Failed",
            "message":"Org Setting deleted",
            "data":"Org Setting  deleted"
        },status=HTTP_200_OK)

class GetOrgSettings(AuthenticatedAPIView):
    serializer_class = IpfilteringSetting
    def get(self,request,orgregno,format=None):
        """
        Get IP Range by Organization
        """
        one_setting = OrganizationSetting.objects.filter(organization=orgregno)
        setting = IpfilteringSetting(one_setting,many=True)
        return Response(setting.data,status=HTTP_200_OK)


class CreateIPrange(AuthenticatedAPIView):
    serializer_class = IpAddresSerialzier
    def post(self,request,format=None):
        """
        Create a Organization IP address filter
        """
        organizationIP = IpAddresSerialzier(data = request.data)
        if organizationIP.is_valid():
            organizationIP.save()
            return Response(organizationIP.data,status=HTTP_200_OK)
        else:
            print(organizationIP.errors)
            return Response({
                "status":"Failed",
                "message":"Organzation IP Exists/Not Valid",
                "data":"Organzation  IP Exists/Not Valid"
            },status=HTTP_400_BAD_REQUEST)

class UpdateIPrange(AuthenticatedAPIView):
    serializer_class = IpAddresSerialzier
    def patch(self,request,iprangeid,format=None):
        """
        Update IP Range by Id
        """
        one_iprange = IpAddress.objects.get(id=iprangeid)
        iprange = IpAddresSerialzier(one_iprange,data=request.data)
        if iprange.is_valid():
            iprange.save()
            return Response(iprange.data,status=HTTP_200_OK)
        else:
            return Response({
                "status":"Failed",
                "message":"IP range Not Updated",
                "data":"IP range Not Updated"
            },status=HTTP_400_BAD_REQUEST)

class DeleteIPrange(AuthenticatedAPIView):
    serializer_class = IpAddresSerialzier
    def delete(self,request,iprangeid,format=None):
        """
        Delete  IP Range by Id
        """
        IpAddress.objects.filter(id=iprangeid).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)

class GetOrgIPrange(AuthenticatedAPIView):
    serializer_class = IpAddresSerialzier
    def get(self,request,orgregno,format=None):
        """
        Get IP Range by Organization
        """
        one_iprange = IpAddress.objects.filter(organization=orgregno)
        iprange = IpAddresSerialzier(one_iprange,many=True)
        return Response(iprange.data,status=HTTP_200_OK)

class CreateDepartment(APIView):
    serializer_class = DepartmentSerializer
    def get(self,request,format=None):
        """
        Get Department
        """
        departments = Department.objects.all()
        all_dep = DepartmentSerializer(departments,many=True)
        return Response(all_dep.data,status=HTTP_200_OK)
     
    def post(self,request,format=None):
        department = DepartmentSerializer(data = request.data)
        if department.is_valid():
            department.save()
            return Response(department.data,status=HTTP_200_OK)
        else:
            print(department.errors)
            return Response({
                "status":"Failed",
                "message":"department Exists/Not Valid",
                "data":"department Exists/Not Valid"
            },status=HTTP_400_BAD_REQUEST)


class UpdateDepartment(APIView):
    serializer_class = DepartmentSerializer
    def patch(self,request,departmentid,format=None):
        """
        Update IP Range by Id
        """
        one_department = Department.objects.get(id=departmentid)
        department = DepartmentSerializer(one_department,data=request.data,partial=True)
        if department.is_valid():
            department.save()
            return Response(department.data,status=HTTP_200_OK)
        else:
            return Response({
                "status":"Failed",
                "message":"Department Not Updated",
                "data":"Department Not Updated"
            },status=HTTP_400_BAD_REQUEST)

    def delete(self,request,departmentid,format=None):
        """
        Delete  Department by Id
        """
        Department.objects.filter(id=departmentid).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)
