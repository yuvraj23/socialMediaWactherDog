from rest_framework import serializers
from account.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':"password"},write_only=True)
    class Meta:
        model=User
        fields=["email","name","password","password2","tc"]
        extra_kwargs={
            "password":{'write_only':True},

        }

    def validate(self, attrs):
        password=attrs.get("password")
        password2=attrs.get("password2")
        if(password != password2):
            raise serializers.ValidationError("Password and confirm password didn't match")
        return attrs
    

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    


class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        fields=["email","password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","name","email","password"]


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=255,style={'input_type':'password'},
                                   write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},
                                   write_only=True)
    
    class Meta:
        model=User
        fields=['password',"password2"]

    def validate(self, attrs):
        user=self.context.get('user')
        password =attrs.get('password')
        password2 =attrs.get('password2')
        if(password != password2):
            raise serializers.ValidationError("Password and confirm password didn't match")
        user.set_password(password)
        user.save()
        return attrs
    
class LogoutSerializer(serializers.Serializer):
    pass  # No fields are required for logout


from .models import YoutubeConfig
class YoutubeConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = YoutubeConfig
        fields = ['user', 'api_key', 'channel_id']

    


