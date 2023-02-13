from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK)
from rest_framework.response import Response
from eboard_system.views import AuthenticatedAPIView
from accounts.models import User
from voting.serializers import VotingQuestionSerializer, VoteSerializer
from voting.models import VotingQuestion, Votes
from rest_framework.views import APIView
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from eboard_system import settings
from sendgrid.helpers.mail import Mail
from eboard_system.utils import send_email
# # Create your views here.

class CreateQuestion(AuthenticatedAPIView):
    serializer_class = VotingQuestionSerializer
    def post(self,request,format=None):
        """
        Create a Question
        """
        one_user = User.objects.get(id=request.data['created_by'])
        members = list(request.data['voters'])
        question = VotingQuestionSerializer(data = request.data)
        if question.is_valid():
            n = question.save(created_by=one_user,voters=members)
            voteID = n.id
            print(voteID)
            vote_link = "http://127.0.0.1:8000/api/voting/{0}/".format(voteID)
            if request.data['sendEmail']:

                subject = "Voter Invitation"
                html_message =  f"<p>You have been invited for a vote on E-Board. Click the link below to see the vote details</p><br><button><a href='{vote_link}'>Open Vote</a></button>"            

                # loop via all emails
                user_emails = []
                for user in members:
                    one_user = User.objects.get(id=user)
                    user_emails.append(one_user.email)

                #send verification code
                message = Mail(
                    from_email=settings.EMAIL_HOST_USER, 
                    to_emails=user_emails, 
                    subject=subject,
                    html_content=html_message
                    )

                send_user_email = send_email(message)
                return Response(question.data,status=HTTP_200_OK)
            else:
                return Response(question.data,status=HTTP_200_OK)
        else:
            print(question.errors)
            return Response({
                "status":"Failed",
                "message":"question not created",
                "data":"question not created"
            },status=HTTP_400_BAD_REQUEST)

class UpdateQuestionById(AuthenticatedAPIView):
    serializer_class = VotingQuestionSerializer
    def patch(self,request,questionid,format=None):
        """
        Update Question by Id
        """
        one_question = VotingQuestion.objects.filter(id=questionid).first()
        question = VotingQuestionSerializer(one_question,data=request.data)
        if request.data['voters']:
            members = list(request.data['voters'])
            if question.is_valid():
                question.save(voters=members)
                return Response(question.data,status=HTTP_200_OK)
            else:
                return Response({
                    "status":"Failed",
                    "message":"question Not Updated",
                    "data":"question Not Updated"
                },status=HTTP_400_BAD_REQUEST)
        else:
            if question.is_valid():
                question.save()
                return Response(question.data,status=HTTP_200_OK)
            else:
                return Response({
                    "status":"Failed",
                    "message":"question Not Updated",
                    "data":"question Not Updated"
                },status=HTTP_400_BAD_REQUEST)

class DeleteQuestionById(AuthenticatedAPIView):
    serializer_class = VotingQuestionSerializer
    def delete(self,request,questionid,format=None):
        """
        Delete question by Id
        """
        one_question = VotingQuestion.objects.filter(id=questionid).delete()
        return Response({
            "status":"OK",
            "message":"Deleted Successfuly",
            "data":"Deleted Successfuly"
        },status=HTTP_200_OK)
        

class GetQuestionById(AuthenticatedAPIView):
    serializer_class = VotingQuestionSerializer
    def get(self,request,questionid,format=None):
        """
        Get question by Id
        """
        one_question = VotingQuestion.objects.filter(id=questionid)
        question = VotingQuestionSerializer(one_question,many=True)
        return Response(question.data,status=HTTP_200_OK)

class GetAllQuestions(AuthenticatedAPIView):
    serializer_class = VotingQuestionSerializer
    def get(self,request,format=None):
        """
        Get all question
        """
        all_questions = VotingQuestion.objects.all()
        print(all_questions)
        question = VotingQuestionSerializer(all_questions,many=True)
        return Response(question.data,status=HTTP_200_OK)

class QuestionVote(AuthenticatedAPIView):
    serializer_class = VoteSerializer
    def post(self,request,format=None):
        """
        Create a Vote
        """
        pushed_vote = request.data['vote']
        one_user = User.objects.get(id=request.data['voter'])
        one_voting_question = VotingQuestion.objects.get(id=request.data['voting_question'])
        user_vote = Votes.objects.filter(voter=one_user,voting_question=one_voting_question)

        total_yes = Votes.objects.filter(voting_question=one_voting_question,vote=1).count()
        print(total_yes)

        total_no = Votes.objects.filter(voting_question=one_voting_question,vote=0).count()
        print(total_no)

        total_abstain = Votes.objects.filter(voting_question=one_voting_question,vote=2).count()
        print(total_abstain)

        total_voters = one_voting_question.voters.count()
        print(total_voters)

        if user_vote:
            return Response({
                "status":"Failed",
                "Message":"You have already voted",
                "data":"You have already votesd"
            })
        else:
            print(one_voting_question.voters.all())
            if one_user in one_voting_question.voters.all():
                vote = VoteSerializer(data = request.data)
                if vote.is_valid():
                    if pushed_vote == 0:
                        one_voting_question.no_votes += 1
                        one_voting_question.no_percentage = ((total_no+1)/total_voters)*100
                    elif pushed_vote == 1:
                        one_voting_question.yes_votes += 1
                        one_voting_question.yes_percentage = ((total_yes+1)/total_voters)*100
                    elif pushed_vote == 2:
                        one_voting_question.abstain_votes += 1
                        one_voting_question.abstain_percentage = ((total_abstain+1)/total_voters)*100
                    
                    one_voting_question.save()
                    vote.save(voter=one_user,voting_question=one_voting_question)
                    return Response(vote.data,status=HTTP_200_OK)
                else:
                    print(vote.errors)
                    return Response({
                        "status":"Failed",
                        "message":"vote not created",
                        "data":"vote not created"
                    },status=HTTP_400_BAD_REQUEST)
            else:
                return Response({
                    "status":"Failed",
                    "message":"Not Allowed to vote",
                    "data":"Not Allowed to vote"
                },status=HTTP_400_BAD_REQUEST)


class GetVoteByQuestion(AuthenticatedAPIView):
    serializer_class = VoteSerializer
    def get(self,request,questionid,format=None):
        """
        Get all question
        """
        all_votes = Votes.objects.filter(voting_question=questionid)
        print(all_votes)
        vote = VoteSerializer(all_votes,many=True)
        return Response(vote.data,status=HTTP_200_OK)

class GetQuestionVotes(AuthenticatedAPIView):
    serializer_class = VoteSerializer
    def get(self,request,questionid,vote,format=None):
        """
        Get Votes for question
        """
        one_voting_question = VotingQuestion.objects.get(id=questionid)
        all_votes = Votes.objects.filter(voting_question=one_voting_question,vote=vote)
        print(all_votes)
        vote = VoteSerializer(all_votes,many=True)
        return Response(vote.data,status=HTTP_200_OK)