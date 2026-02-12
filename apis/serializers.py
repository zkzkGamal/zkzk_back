from rest_framework import serializers 
from .models import *
from django.contrib.auth.models import User

# login user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

# create user
class Registration(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password' ,'first_name','last_name')
        extra_kwargs = {'password': {'write_only': True}}
    
# get all post data
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectPost
        exclude = ('created', )

# get all tags
class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'

# comment section 
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = post_comment
        exclude = ('created', )

# profile serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__' 

# profile serializer
class notifySerializer(serializers.ModelSerializer):
    class Meta:
        model = notify_user
        fields = '__all__' 

class my_resumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = my_resume
        fields = '__all__'
    