from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
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
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['id','username','email']
        read_only_fields = ['id',]
        
