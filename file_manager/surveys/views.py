from django.shortcuts import render
from eboard_system.views import AuthenticatedAPIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_200_OK)
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AddSurveySerialzier, ListSurveySerialzier, QuestionSerialzier, ResponsesSerialzier, RespondentsSerializer
from .models import Survey, SurveyQuestions, SurveyResponses, SurveyRepondents

# Create your views here.


class CreateSurvey(AuthenticatedAPIView):
    serializer_class = AddSurveySerialzier

    def post(self, request, format=None):
        """
        Create a Survey
        """
        one_user = request.user
        one_org = request.user.org_reference_key

        members = list(request.data['permissions'])
        survey = AddSurveySerialzier(data=request.data)
        if survey.is_valid():
            survey.save(survey_created_by=one_user,
                        organization=one_org, permissions=members)
            return Response(survey.data, status=HTTP_200_OK)
        else:
            print(survey.errors)
            return Response({
                "status": "Failed",
                "message": "survey not created",
                "data": "survey not created"
            }, status=HTTP_400_BAD_REQUEST)


class UpdateSurveyById(AuthenticatedAPIView):
    serializer_class = ListSurveySerialzier

    def patch(self, request, surveyid, format=None):
        """
        Update Survey by Id
        """
        one_survey = Survey.objects.filter(id=surveyid).first()
        survey = ListSurveySerialzier(one_survey, data=request.data)
        if request.data['permissions']:
            members = list(request.data['permissions'])
            if survey.is_valid():
                survey.save(permissions=members)
                return Response(survey.data, status=HTTP_200_OK)
            else:
                return Response({
                    "status": "Failed",
                    "message": "survey Not Updated",
                    "data": "survey Not Updated"
                }, status=HTTP_400_BAD_REQUEST)
        else:
            if survey.is_valid():
                survey.save()
                return Response(survey.data, status=HTTP_200_OK)
            else:
                return Response({
                    "status": "Failed",
                    "message": "survey Not Updated",
                    "data": "survey Not Updated"
                }, status=HTTP_400_BAD_REQUEST)


class DeleteSurveyById(AuthenticatedAPIView):
    serializer_class = ListSurveySerialzier

    def delete(self, request, surveyid, format=None):
        """
        Delete survey by Id
        """
        one_survey = Survey.objects.filter(id=surveyid).delete()
        return Response({
            "status": "OK",
            "message": "Deleted Successfuly",
            "data": "Deleted Successfuly"
        }, status=HTTP_200_OK)


class GetAllSurveys(AuthenticatedAPIView):
    serializer_class = ListSurveySerialzier

    def get(self, request, format=None):
        """
        Get all Surveys
        """
        user = request.user
        if user.org_permission == 'Admin':
            all_surveys = Survey.objects.all()
        else:
            all_surveys = Survey.objects.filter(permissions=user)
        print(all_surveys)
        survey = ListSurveySerialzier(all_surveys, many=True)
        return Response(survey.data, status=HTTP_200_OK)

# creating survey questions

class SurveyQuestion(AuthenticatedAPIView):
    serializer_class = QuestionSerialzier

    def post(self, request, format=None):
        """
        Create a Survey Question
        """
        survey_id = request.data['survey_id']
        one_survey = Survey.objects.get(id=survey_id)
        for i in request.data['questions']:
            survey_question = QuestionSerialzier(data=i)
            response_array = []
            if survey_question.is_valid():
                survey_question.save(
                    survey=one_survey, responses=response_array)
                responses = list(i['responses'])
                response_array = []
                for i in responses:
                    print("inside response loop")
                    print(i)
                    n = SurveyResponses.objects.create(
                        responses=i['option']
                    )
                    print(n.id)
                    response_array.append(n.id)
                survey_question.save(
                    survey=one_survey, responses=response_array)
                response_array = []
            else:
                print(survey_question.error)
        return Response({
            "status": "OK",
            "message": "Questions Added",
            "data": "Questions Added"
        }, status=HTTP_200_OK)


class UpdateSurveyQuestionById(AuthenticatedAPIView):
    serializer_class = QuestionSerialzier

    def patch(self, request, surveyqnid, format=None):
        """
        Update Survey question by Id
        """
        one_survey_qn = SurveyQuestions.objects.filter(id=surveyqnid).first()
        survey_qn = QuestionSerialzier(one_survey_qn, data=request.data)
        if survey_qn.is_valid():
            survey_qn.save()
            return Response(survey_qn.data, status=HTTP_200_OK)
        else:
            return Response({
                "status": "Failed",
                "message": "survey Not Updated",
                "data": "survey Not Updated"
            }, status=HTTP_400_BAD_REQUEST)


class DeleteSurveyQuestionById(AuthenticatedAPIView):
    serializer_class = QuestionSerialzier

    def delete(self, request, surveyqnid, format=None):
        """
        Delete survey qn by Id
        """
        one_survey_qn = SurveyQuestions.objects.filter(id=surveyqnid).delete()
        return Response({
            "status": "OK",
            "message": "Deleted Successfuly",
            "data": "Deleted Successfuly"
        }, status=HTTP_200_OK)


class GetAllSurveyQuestionsById(AuthenticatedAPIView):
    serializer_class = QuestionSerialzier

    def get(self, request, surveyid, format=None):
        """
        Get all _survey_questions
        """
        all_survey_questions = SurveyQuestions.objects.filter(survey=surveyid)
        survey_qn = QuestionSerialzier(all_survey_questions, many=True)
        return Response(survey_qn.data, status=HTTP_200_OK)


class UpdateSurveyResponseByQuestion(AuthenticatedAPIView):
    serializer_class = ResponsesSerialzier

    def patch(self, request, surveyqnid, respid, format=None):
        """
        Update Survey question by Id
        """
        qn = SurveyQuestions.objects.get(id=surveyqnid)
        one_survey_resp = SurveyResponses.objects.filter(
            survey_question=qn, id=respid).first()
        survey_resp = ResponsesSerialzier(one_survey_resp, data=request.data)
        if survey_resp.is_valid():
            survey_resp.save()
            return Response(survey_resp.data, status=HTTP_200_OK)
        else:
            return Response({
                "status": "Failed",
                "message": "survey resp Not Updated",
                "data": "survey resp Not Updated"
            }, status=HTTP_400_BAD_REQUEST)


class DeleteSurveyResponseById(AuthenticatedAPIView):
    serializer_class = ResponsesSerialzier

    def delete(self, request, respid, format=None):
        """
        Delete survey resp by Id
        """
        one_survey_resp = SurveyResponses.objects.filter(id=respid).delete()
        return Response({
            "status": "OK",
            "message": "Deleted Successfuly",
            "data": "Deleted Successfuly"
        }, status=HTTP_200_OK)


class SubmitAnswers(AuthenticatedAPIView):
    serializer_class = ResponsesSerialzier

    def patch(self, request, format=None):
        for i in request.data['questions']:
            qn = SurveyQuestions.objects.get(id=i['question_id'])

            if i['question_type'] == 'checkbox':
                answers = list(i['answer'])
                instance = SurveyRepondents.objects.create(
                    survey_question=qn, respondent=request.user)
                instance.selected_responses.set(answers)

            elif i['question_type'] == 'radio':
                answer = [int(x) for x in str(i['answer'])]
                instance = SurveyRepondents.objects.create(
                    survey_question=qn, respondent=request.user)
                instance.selected_responses.set(answer)

            else:
                SurveyRepondents.objects.create(
                    survey_question=qn, respondent=request.user, answer=i['answer'])

        return Response({
            "status": "OK",
            "message": "Submitted Successfuly",
            "data": "Submitted Successfuly"
        }, status=HTTP_200_OK)


class SurveyQuestionAnalytics(AuthenticatedAPIView):
    serializer_class = RespondentsSerializer

    def get(self, request, questionId, format=None):
        try:
            question = SurveyQuestions.objects.get(id=questionId)
            respondants_qn = SurveyRepondents.objects.filter(survey_question=question)
            responses_count = respondants_qn.count()
            statistics = []
            statistics_linear = []
            for question in respondants_qn:
                for response in question.selected_responses.all():
                    data = {}
                    data['id'] = response.id
                    data['answer'] = response.responses
                    data['count'] = 1
                    statistics.append(data)

                if question.survey_question.question_type == 'liner-scale':
                    data = {}
                    data['answer'] = question.answer
                    data['count'] = 1
                    statistics_linear.append(data)

            response_data_linear = []
            for data in statistics_linear:
                if data not in response_data_linear:
                    response_data_linear.append(data)
                else:
                    d = next(item for item in response_data_linear if item == data)
                    d['count'] += 1
            
            response_data = []
            for data in statistics:
                if data not in response_data:
                    response_data.append(data)
                else:
                    d = next(item for item in response_data if item == data)
                    d['count'] += 1

            respondents = RespondentsSerializer(respondants_qn, many=True).data


            res = []
            if len(response_data) > 0:
                res = response_data
            if len(response_data_linear) > 0:
                res = response_data_linear

            json_response = {
                "respondant_count":responses_count,
                "result":respondents,
                "statistics":res
            }

            return Response(json_response, status=HTTP_200_OK)

        except:
            pass


class UserAnswerCheck(AuthenticatedAPIView):
    serializer_class = RespondentsSerializer

    def get(self, request, userid, format=None):
        usr = request.user
        respondants_qn = SurveyRepondents.objects.filter(respondent=usr)
        respondents = RespondentsSerializer(respondants_qn, many=True)
        return Response(respondents.data, status=HTTP_200_OK)


class UserQuestionAnswerCheck(AuthenticatedAPIView):
    serializer_class = RespondentsSerializer

    def get(self, request, userid, surveyid, format=None):
        question = SurveyQuestions.objects.get(id=surveyid)
        usr = User.objects.get(id=userid)
        respondants_qn = SurveyRepondents.objects.filter(
            respondent=usr, survey_question=question)
        respondents = RespondentsSerializer(respondants_qn, many=True)
        return Response(respondents.data, status=HTTP_200_OK)
