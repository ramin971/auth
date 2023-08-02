from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password 
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid refresh_token found in cookie')


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()      # to set as required
    class Meta:
        model = User
        fields = ['id','username','email','password']
        extra_kwargs = {'id':{'read_only':True},'password':{'write_only':True}}

    def validate_password(self,value):
        validate_password(value)
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
    
class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']
        read_only_fields = ['id']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True , write_only=True)
    new_password = serializers.CharField(required=True , write_only=True)

    def validate_old_password(self,value):
        user = self.context['user']
        if not user.check_password(value):
            raise serializers.ValidationError('Your old password was entered incorrectly.')
        return value
    
    def validate_new_password(self,value):
        validate_password(value)
        return value
    
    def save(self, **kwargs):
        user = self.context['user']
        password = self.validated_data['new_password']
        user.set_password(password)
        user.save()
        return user
    



