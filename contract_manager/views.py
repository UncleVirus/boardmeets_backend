from django.shortcuts import render
from .models import ContractDetail, ContractStage, ContractSignature, ContractFeedBack
from .serializers import ContractSerializer, ContractStageSerializer, ContractSignatureSerializer, ContractFeedBackSerializer
from accounts.models import User
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK, HTTP_404_NOT_FOUND)
from rest_framework.views import APIView
from eboard_system.views import AuthenticatedAPIView
from datetime import datetime, timedelta
from eboard_system import settings
from sendgrid.helpers.mail import Mail
from eboard_system.utils import send_email

# Create your views here.


class ContractsList(AuthenticatedAPIView):
    serializer_class = ContractSerializer

    def post(self, request, format=None):
        """
        Post Contract 
        """
        if request.data['created_by']:
            user = User.objects.get(id=request.data['created_by'])
        else:
            user = request.user

        approvers = list(request.data['approvers'])
        permission = list(request.data['permission'])
        signatories = list(request.data['signatories'])

        request.data['duration'] = '0 days'
        contract = ContractSerializer(data=request.data)
        if contract.is_valid():
            new_contract = contract.save(
                created_by=user, approvers=approvers, permission=permission, signatories=signatories)

            date_format_str = '%Y/%d/%m %H:%M:%S'
            start = new_contract.start_date_time
            contract_start = start.strftime(date_format_str)
            end = new_contract.end_date_time
            contract_end = end.strftime(date_format_str)

            start_date = datetime.strptime(
                str(contract_start), date_format_str)
            end_date = datetime.strptime(str(contract_end), date_format_str)

            contract_duration = end_date - start_date

            duration = "%d days" % contract_duration.days
            contract.save(duration=duration)

            # loop via all emails
            subject = "RE: eSignature document!"
            html_message = f"<p>You assigned to sign to this this document kindly click on the link below to sign.</p>"

            user_emails = []
            for user in signatories:
                one_user = User.objects.get(id=user)
                user_emails.append(one_user.email)

            # send verification code
            message = Mail(
                from_email=settings.EMAIL_HOST_USER,
                to_emails=user_emails,
                subject=subject,
                html_content=html_message
            )

            send_user_email = send_email(message)

            return Response(contract.data, status=HTTP_200_OK)
        else:
            print(contract.errors)
            return Response({
                "status": "Failed",
                "message": "contract not created",
                "data": "contract not created"
            }, status=HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        """
        Get Contract List
        """
        user = request.user
        if user.org_permission == 'Admin':
            contracts = ContractDetail.objects.all()
        else:
            contracts = ContractDetail.objects.filter(permission=user)

        contract_list = ContractSerializer(contracts, many=True)
        return Response(contract_list.data, status=HTTP_200_OK)


class GetContractsBySignatory(AuthenticatedAPIView):
    serializer_class = ContractSerializer

    def get(Self, request, format=None):

        user = request.user
        contracts = ContractDetail.objects.filter(signatories=user)
        contract_list = ContractSerializer(contracts, many=True)
        return Response(contract_list.data, status=HTTP_200_OK)


class GetContractsByApprover(AuthenticatedAPIView):
    serializer_class = ContractSerializer

    def get(Self, request, format=None):

        user = request.user
        contracts = ContractDetail.objects.filter(approvers=user)
        contract_list = ContractSerializer(contracts, many=True)
        return Response(contract_list.data, status=HTTP_200_OK)


class ContractUpdate(AuthenticatedAPIView):
    serializer_class = ContractSerializer

    def patch(self, request, contractid, format=None):
        one_contract = ContractDetail.objects.get(id=contractid)
        approvers = list(request.data['approvers'])
        permission = list(request.data['permission'])
        signatories = list(request.data['signatories'])
        contract = ContractSerializer(
            one_contract, data=request.data, partial=True)
        if contract.is_valid():
            contract.save(approvers=approvers,
                          permission=permission, signatories=signatories)
            return Response(contract.data, status=HTTP_200_OK)
        else:
            print(contract.errors)
            return Response({
                "status": "Failed",
                "message": "contract Not Updated",
                "data": "contract Not Updated"
            }, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, contractid, format=None):
        """
        Delete contract by Id
        """
        ContractDetail.objects.filter(id=contractid).delete()
        return Response({
            "status": "OK",
            "message": "Deleted Successfuly",
            "data": "Deleted Successfuly"
        }, status=HTTP_200_OK)


class ContractByStatus(AuthenticatedAPIView):
    serializer_class = ContractSerializer

    def get(self, request, percentage, format=None):
        contracts = ContractDetail.objects.filter(
            percentage_approval=percentage)
        contract_list = ContractSerializer(contracts, many=True)
        return Response(contract_list.data, status=HTTP_200_OK)


class ContractStageUpdate(AuthenticatedAPIView):
    serializer_class = ContractStageSerializer

    def post(self, request, format=None):
        # getting parent object
        if request.data['action_taker']:
            user = request.data['action_taker']
        else:
            user = request.user

        parent_contract = ContractDetail.objects.get(
            id=request.data['contract_id'])

        # get action taker
        action_taker = User.objects.get(id=user)
        try:
            # check if the action taker has already actioned on this contract
            approver_object = ContractStage.objects.filter(
                parent_contract=parent_contract, action_taker=action_taker)
            if approver_object:
                print("user already made a vote")
                one_contract_stage = ContractStage.objects.get(
                    parent_contract=parent_contract, action_taker=action_taker)
                contract_stage = ContractStageSerializer(
                    one_contract_stage, data=request.data, partial=True)
                if contract_stage.is_valid():
                    if parent_contract.approvers.filter(id=request.data['action_taker']).exists():
                        contract_stage.save()
                        return Response(contract_stage.data, status=HTTP_200_OK)
                    return Response({
                        "status": "Failed",
                        "message": "You are not athorized to update this contract",
                    }, status=HTTP_400_BAD_REQUEST)
                else:
                    return Response({
                        "status": "Failed",
                        "message": "user vote not updated",
                        "data": "user vote not updated"
                    }, status=HTTP_400_BAD_REQUEST)
            else:
                # save the contract stage object for new action
                contract_stage = ContractStageSerializer(data=request.data)
                if contract_stage.is_valid():
                    if parent_contract.approvers.filter(id=request.data['action_taker']).exists():

                        contract_stage.save(
                            parent_contract=parent_contract, action_taker=action_taker)

                        # calculate the percentage of actions done on the contract by approvers formula is
                        # (number of conracts action done/total number of approvers)*100
                        # no_of_approvers = parent_contract.approvers.count()

                        contract_objects = ContractStage.objects.filter(
                            parent_contract=parent_contract).count()
                        no_of_approvers = parent_contract.approvers.count()
                        percentage_approval = (
                            contract_objects/no_of_approvers) * 100
                        print(percentage_approval)
                        ContractDetail.objects.filter(id=request.data['contract_id']).update(
                            percentage_approval=percentage_approval)
                        return Response(contract_stage.data, status=HTTP_200_OK)

                    return Response({
                        "status": "Failed",
                        "message": "You are not athorized to approve this contract",
                    }, status=HTTP_400_BAD_REQUEST)
                else:
                    print(contract_stage.errors)
                    return Response({
                        "status": "Failed",
                        "message": "Invalid input",
                    }, status=HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "status": "Failed",
                "message": "contract_stage Not Updated/User not approver",
                "data": "contract_stage Not Updated/User not approver"
            }, status=HTTP_400_BAD_REQUEST)


class ContractAllStage(AuthenticatedAPIView):
    serializer_class = ContractStageSerializer

    def get(self, request, contractid, format=None):
        """
        Get Contract List
        """
        parent_contract = ContractDetail.objects.get(id=contractid)
        approval_count = parent_contract.approvers.count()
        contracts = ContractStage.objects.filter(
            parent_contract=parent_contract)
        if contracts:
            approved_count = len(contracts)
            contract_list = ContractStageSerializer(contracts, many=True)
            data = {'approval_count': approval_count,
                    'approved_count': approved_count, 'res': contract_list.data}
            return Response(data, status=HTTP_200_OK)


class CreateContractSignature(AuthenticatedAPIView):
    serializer_class = ContractSignatureSerializer

    def post(self, request, contractid, format=None):
        """
        create Contract signature
        """
        contract = ContractDetail.objects.get(id=contractid)
        sfdf_string = request.data['xfdfString']

        if contract is not None and sfdf_string is not None:
            signature_instance = ContractSignature.objects.create(
                xfdf_string=sfdf_string,
                contract=contract,
                signed_at=datetime.now()
            )

            if signature_instance:
                response = ContractSignatureSerializer(signature_instance).data
                return Response(response, status=200)

            return Response({"details": "Something went wrong. "}, status=400)
        return Response({"details": "bad request. "}, status=404)


class SigningContract(AuthenticatedAPIView):
    serializer_class = ContractSignatureSerializer

    def post(self, request, contractid, format=None):
        """
        create Contract signature
        """
        user = request.user
        contract = ContractDetail.objects.get(id=contractid)
        sfdf_string = request.data['sfdf_string']
        exist_signature = ContractSignature.objects.filter(
            signer=user).exists()

        if contract is not None and sfdf_string is not None:
            if contract.signatories.filter(id=user.id).exists():
                if not exist_signature:

                    signature_instance = ContractSignature.objects.create(
                        xfdf_string=sfdf_string,
                        contract=contract,
                        signer=user,
                        is_updated=True,
                        signed_at=datetime.now()
                    )

                    if signature_instance:
                        response = ContractSignatureSerializer(
                            signature_instance).data
                        return Response(response, status=200)
                return Response({"details": "You already signed. "}, status=400)

            return Response({"details": "You are not authorized. "}, status=400)
        return Response({"details": "bad request. "}, status=404)


class GetContractSignatureByContractId(AuthenticatedAPIView):
    serializer_class = ContractSignatureSerializer

    def get(self, request, contractid, format=None):
        """
        create Contract signature
        """
        user = request.user
        user_email = user.email
        print('...............', user_email)
        contract = ContractDetail.objects.get(id=contractid)

        if contract is not None:
            signature_instance = ContractSignature.objects.filter(
                contract=contract, xfdf_string__contains=user_email)
            if signature_instance:
                response = ContractSignatureSerializer(
                    signature_instance, many=True)
                return Response(response.data, status=200)

            return Response([], status=400)
        return Response({"details": "Data not found. "}, status=404)


class GetContractSignatureAnalytics(AuthenticatedAPIView):
    serializer_class = ContractSignatureSerializer

    def get(self, request, contractid, format=None):
        """
        create Contract signature
        """
        contract = ContractDetail.objects.get(id=contractid)

        if contract is not None:
            signatories_count = contract.signatories.count()

            signature_instance = ContractSignature.objects.filter(
                contract=contract, is_updated=True)

            if signature_instance:
                signature_count = len(signature_instance)
                response = ContractSignatureSerializer(
                    signature_instance, many=True)

                data = {'signatories_count': signatories_count,
                        'signed_count': signature_count, 'res': response.data}
                return Response(data, status=200)

            return Response([], status=400)
        return Response({"details": "Data not found. "}, status=404)


class CreateContractFeedBack(AuthenticatedAPIView):
    serializer_class = ContractFeedBackSerializer

    def post(self, request, contractid, format=None):
        """
        create Contract Feedback
        """
        contract = ContractDetail.objects.get(id=contractid)

        if contract is not None and request.data is not None:
            # create instance here
            feedback_instance = ContractFeedBack.objects.create(
                title=request.data['title'],
                comment=request.data['comment'],
                status=request.data['status'],
                contract=contract,
                created_by=request.user
            )
            if feedback_instance:
                response = ContractFeedBackSerializer(feedback_instance).data
                return Response(response, status=200)

            return Response({"details": "Something went wrong. "}, status=400)
        return Response({"details": "bad request. "}, status=404)


class GetContractFeedBacks(AuthenticatedAPIView):
    serializer_class = ContractFeedBackSerializer

    def get(self, request, contractid, format=None):
        """
        create Contract signature
        """
        contract = ContractDetail.objects.get(id=contractid)

        if contract is not None:
            feedback_instance = ContractFeedBack.objects.filter(
                contract=contract)

            if feedback_instance:
                response = ContractFeedBackSerializer(
                    feedback_instance, many=True)
                return Response(response.data, status=200)

            return Response([], status=400)
        return Response({"details": "Data not found. "}, status=404)


class ContractFeedBackUpdate(AuthenticatedAPIView):
    serializer_class = ContractFeedBackSerializer

    def patch(self, request, feedbackId, format=None):
        # update feedback by id
        feedback = ContractFeedBack.objects.get(id=feedbackId)

        contract_feedback = ContractFeedBackSerializer(
            feedback, data=request.data, partial=True)
        if contract_feedback.is_valid():
            contract_feedback.save()
            return Response(contract_feedback.data, status=HTTP_200_OK)
        else:
            return Response({
                "status": "Failed",
                "message": "Feedback Not Updated",
            }, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, feedbackId, format=None):
        """
        Delete feedback by Id
        """
        print('====', feedbackId)
        ContractFeedBack.objects.get(id=feedbackId).delete()
        return Response({
            "status": "OK",
            "message": "Deleted Successfuly",
        }, status=HTTP_200_OK)
