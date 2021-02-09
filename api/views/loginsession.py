from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
import hashlib
import datetime
from dateutil.parser import parse
from api.models import User, LoginSession
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
from django.db.models import Q
from mongoengine.queryset.visitor import Q
from lib.TGMT.TGMTemail import SendEmailInternal
import api.auth
from api.views.loginsession import *

####################################################################################################

@api_view(["POST"])
def GetLoginSession(request):
    try:
        _user_id = request.POST.get('user_id') 
        _userID = request.POST.get('userID')
        _building_id = request.POST.get('building_id')
        _fromDateStr = request.POST.get("fromDate")
        _toDateStr = request.POST.get("toDate")

        if(_fromDateStr == None or _fromDateStr == "" or
            _toDateStr == None or _toDateStr == "" or
            _building_id == None or _building_id == "" or
            _userID == None or _userID == ""):
            return Response(
            {'Error': "Thiếu tham số"},
            status=ERROR_CODE,
            content_type="application/json"
            )

        _fromDate = parse(_fromDateStr)
        _toDate = parse(_toDateStr) +  datetime.timedelta(days=1)

        if(_fromDate == None or _toDate == None):
            return Response(
            {'Error': "Thiếu ngày "},
            status=ERROR_CODE,
            content_type="application/json"
            )

        if(_building_id == "all"):
            histories = GetLoginSession.objects(loginTime__gte=_fromDate, loginTime__lt=_toDate)
        else:
            histories = GetLoginSession.objects(building_id = _building_id, loginTime__gte=_fromDate, loginTime__lt=_toDate)

        if(_userID != "all"):
            histories = histories(user_id=_userID)


        return Response(
            json.loads(histories.to_json()),
            status=SUCCESS_CODE,
            content_type="application/json"
            )
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))

####################################################################################################

#demo how to verify token
@api_view(["POST"])
def verifyToken(request):
    try:
        _token = request.POST.get('token')
        loginSession = FindLoginSession(_token)
        return JsonResponse(loginSession.to_json())
    except Exception as e:        
        return ErrorResponse("Có lỗi: " + str(e))


####################################################################################################

def FindLoginSession(token):
    jwtDecoded = api.auth.decode(token)
    loginSession = LoginSession.objects.get(pk=jwtDecoded['loginSession_pk'], isDeleted=False)
    return loginSession