from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import UserRegistrationSerializer

class UserRegistrationView(APIView):

    def post(self,request,format=None):
        serailizer=UserRegistrationSerializer(data=request.data)
        if serailizer.is_valid(raise_exception=True):
            user=serailizer.save()
            return Response({'msg':"User creation success..","user : ":user},
                            status=201)
        return Response({'msg':"User creation failed","error":serailizer.error_messages})

