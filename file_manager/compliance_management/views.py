from django.shortcuts import render
from rest_framework.response import Response
from eboard_system.views import AuthenticatedAPIView
from rest_framework.views import APIView
from accounts.models import User
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK)
from .models import ComplianceDetail,ChecklistDetail
from .serializers import ComplianceDetailsSerialzier, ComplianceCheckListSerialzier

# Create your views here.
class GetCompliances(AuthenticatedAPIView):
    serializer_class = ComplianceDetailsSerialzier
    def get(self,request,format=None):
        compliances = ComplianceDetail.objects.all()
        all_compliance = ComplianceDetailsSerialzier(compliances,many=True)
        return Response(all_compliance.data,status=HTTP_200_OK)

class GetChecklistByCompliance(AuthenticatedAPIView):
    serializer_class = ComplianceCheckListSerialzier
    def get(self,request,compliance_id,format=None):
        one_compliance = ComplianceDetail.objects.get(id=compliance_id)
        check_lists = ChecklistDetail.objects.filter(parent_compliance=one_compliance)
        all_compliance_checklists = ComplianceCheckListSerialzier(check_lists,many=True)
        return Response(all_compliance_checklists.data,status=HTTP_200_OK)

class CreateCompliance(AuthenticatedAPIView):
    serializer_class = ComplianceDetailsSerialzier
    def post(self,request,format=None):
        new_compliance = ComplianceDetailsSerialzier(data=request.data)
        if new_compliance.is_valid():
            new_compliance.save()
            return Response(new_compliance.data,status=HTTP_200_OK)
        else:
            print(new_compliance.errors)
            return Response({
                "status":"Failed",
                "message":"Compliance not created",
                "data":"Compliance not created"
            },status=HTTP_400_BAD_REQUEST)

class CreateChecklist(AuthenticatedAPIView):
    serializer_class = ComplianceCheckListSerialzier
    def post(self,request,format=None):
        compliance = ComplianceDetail.objects.get(id=request.data['compliance_id'])
        print(compliance)
        for i in request.data['checks']:
            new_checklist = ComplianceCheckListSerialzier(data=i)
            if new_checklist.is_valid():
                new_checklist.save(parent_compliance=compliance)
            else:
                print(new_checklist.errors)
                return Response({
                    "status":"OK",
                    "message":"Checklist Not Added",
                    "data":"Checklist Not Added"
                },status=HTTP_400_BAD_REQUEST)
        return Response({
                    "status":"OK",
                    "message":"Checklist  Added",
                    "data":"Checklist Added"
                },status=HTTP_200_OK)

class MarkChecklist(AuthenticatedAPIView):
    serializer_class = ComplianceCheckListSerialzier
    def patch(self,request,compliance_id,checklist_id,format=None):
        one_compliance=ComplianceDetail.objects.get(id=compliance_id)
        one_checklist = ChecklistDetail.objects.get(parent_compliance=one_compliance,id=checklist_id)
        request.data['check_name'] = one_checklist.check_name
        updated_check = ComplianceCheckListSerialzier(one_checklist,data=request.data)
        if updated_check.is_valid():
            updated_check.save()
            #update the parent score
            passed_checks = ChecklistDetail.objects.filter(parent_compliance=one_compliance,check_status=True).count()
            total_checks = ChecklistDetail.objects.filter(parent_compliance=one_compliance).count()
            print(passed_checks)
            print(total_checks)
            pass_rate = (passed_checks/total_checks) * 100
            print(int(pass_rate))
            one_compliance=ComplianceDetail.objects.filter(id=compliance_id).update(compliance_score=pass_rate)

            return Response(updated_check.data,status=HTTP_200_OK)
        else:
            print(updated_check.errors)
            return Response({
                "status":"Failed",
                "message":"Checklist Not Updated",
                "data":"Checklist Not Updated"
            },status=HTTP_400_BAD_REQUEST)

class UpdateCompliance(AuthenticatedAPIView):
    serializer_class = ComplianceDetailsSerialzier
    def patch(self,request,compliance_id,format=None):
        one_compliance=ComplianceDetail.objects.get(id=compliance_id)
        compliance_update = ComplianceDetailsSerialzier(one_compliance,data=request.data)
        if compliance_update.is_valid():
            compliance_update.save()
            return Response(compliance_update.data,status=HTTP_200_OK)
        else:
            return Response({
                "status":"Failed",
                "message":"Compliance Not Updated",
                "data":"Compliance Not Updated"
            },status=HTTP_400_BAD_REQUEST)

class DeleteComplianceById(AuthenticatedAPIView):
    serializer_class = ComplianceDetailsSerialzier
    def delete(self,request,compliance_id,format=None):
        """
        Delete Compliance by Id
        """
        ComplianceDetail.objects.filter(id=compliance_id).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)

class UpdateComplianceChecklist(AuthenticatedAPIView):
    serializer_class = ComplianceCheckListSerialzier
    def patch(self,request,checklist_id,format=None):
        one_compliance_check=ChecklistDetail.objects.get(id=checklist_id)
        complianc_check_update = ComplianceCheckListSerialzier(one_compliance_check,data=request.data)
        if complianc_check_update.is_valid():
            complianc_check_update.save()
            return Response(complianc_check_update.data,status=HTTP_200_OK)
        else:
            return Response({
                "status":"Failed",
                "message":"Compliance Checklist Not Updated",
                "data":"Compliance Checklist Not Updated"
            },status=HTTP_400_BAD_REQUEST)

class DeleteComplianceChecklistById(AuthenticatedAPIView):
    serializer_class = ComplianceCheckListSerialzier
    def delete(self,request,checklist_id,format=None):
        """
        Delete Compliance Check list by Id
        """
        ChecklistDetail.objects.filter(id=checklist_id).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)
