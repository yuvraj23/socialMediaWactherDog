from pstats import Stats
import statistics
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from account.serializers import UserChangePasswordSerializer, UserLoginSerializer, UserRegistrationSerializer,UserProfileSerializer
from django.contrib.auth import authenticate
from account.renders import UserErrors
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .YoutubeFetcher import Youtube


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes=[UserErrors,]
    def post(self,request,format=None):
        serailizer=UserRegistrationSerializer(data=request.data)
        if serailizer.is_valid(raise_exception=True):
            user=serailizer.save()
            token=get_tokens_for_user(user)
            return Response({'token':token,'msg':"User creation success.."},status=200)
        return Response({'msg':"User creation failed","error":serailizer.error_messages})
    

class UserLoginView(APIView):
    renderer_classes=[UserErrors,]
    def post(self,request,format=None):
        serailizer=UserLoginSerializer(data=request.data)
        if serailizer.is_valid(raise_exception=True):
            email=serailizer.data.get('email')
            password=serailizer.data.get('password')
            user=authenticate(email=email,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                
                return Response({'token':token,'msg':"Login success.."},status=200)
            else:
                return Response({'errors':{'non_field_errors':['Email or password is not valid']}},status=404)
            
class ProfileView(APIView):
    renderer_classes=[UserErrors,]
    permission_classes=[IsAuthenticated,]
    def get(self,request,format=None):
        serailizer=UserProfileSerializer(request.user)
        return  Response({'msg':"Profile data fetched..","data":serailizer.data},status=200)
    

class UserChangePasswordView(APIView):
    renderer_classes=[UserErrors,]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serailizer=UserChangePasswordSerializer(data=request.data,context={'user':request.user})

        if serailizer.is_valid(raise_exception=True):
            return Response({"msg":"Password changed successfully"},status=200)
        return Response({'msg':"Bad Request"})
    




from rest_framework import generics, status
from rest_framework.response import Response
from .models import YoutubeConfig
from .serializers import YoutubeConfigSerializer
from .models import User  # Assuming you have a custom User model

class YoutubeConfigCreate(generics.CreateAPIView):
    serializer_class = YoutubeConfigSerializer
    queryset = YoutubeConfig.objects.all()

    def create(self, request, *args, **kwargs):
        user_email = request.data.get('user_mail_id')
        api_key = request.data.get('api_key')
        channel_id = request.data.get('channel_id')

        # Get the user object by email
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            return Response({"error": "User not found with the given email"}, status=status.HTTP_404_NOT_FOUND)

        # Create YoutubeConfig instance
        youtube_config_data = {
            'user': user.id,
            'api_key': api_key,
            'channel_id': channel_id
        }

        serializer = self.get_serializer(data=youtube_config_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class YoutubeMetricsView(APIView):
    renderer_classes = [UserErrors, ]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user_email =request.data.get('user_mail_id')
        try:
            user = get_object_or_404(User, email=user_email)
            youtube_configs = YoutubeConfig.objects.filter(user=user)

            # Serialize the queryset
            serializer = YoutubeConfigSerializer(youtube_configs, many=True)
            serialized_data = serializer.data

            # Print or use the serialized data as needed
            useYoutubeAccounts={}
            for item in serialized_data:
                api_key = item['api_key']
                channel_id = item['channel_id']
                youtubeClient=Youtube(api_key)
                result=youtubeClient.get_channel_metrics(channel_id)
                useYoutubeAccounts[channel_id]=result
            return Response({"msg": "Success", "data": useYoutubeAccounts}, status=200)

        except Exception as e:
            return Response({"error": e}, status=status.HTTP_404_NOT_FOUND)



class UserYoutubeAllChannel(APIView):
    renderer_classes = [UserErrors, ]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user_email =request.data.get('user_mail_id')
        try:
            user = get_object_or_404(User, email=user_email)
            youtube_configs = YoutubeConfig.objects.filter(user=user)
            serializer = YoutubeConfigSerializer(youtube_configs, many=True)
            serialized_data = serializer.data

            # uncomment this line when you want to real data as of commented this line because this invoking youtube apis
            # we don't need to invoked for testing purpose

            # useYoutubeAccounts={}
            # for item in serialized_data:
            #     api_key = item['api_key']
            #     channel_id = item['channel_id']
            #     youtubeClient=Youtube(api_key)
            #     result=youtubeClient.get_channel_metrics(channel_id)
            #     useYoutubeAccounts[channel_id]=result
            useYoutubeAccounts={
                "UCFfkrMKhD1gBGprCetCi5aQ": {
                    "channel_name": "GamerWare",
                    "subscriber_count": 447,
                    "total_video_count": 441,
                    "total_likes": 9653,
                    "total_dislikes": 0,
                    "total_money_earned": 0
                },
                "UCbbMow_bYRwnAaysU9qpNGw": {
                    "channel_name": "CodeSync",
                    "subscriber_count": 8,
                    "total_video_count": 16,
                    "total_likes": 8,
                    "total_dislikes": 0,
                    "total_money_earned": 0
                }
            }
            return Response({"youtube_channel_list": useYoutubeAccounts}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

