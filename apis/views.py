from django.shortcuts import render
from django.http import JsonResponse

# filter lib
from django_filters.rest_framework import DjangoFilterBackend

# restframework lib
from rest_framework import mixins, generics, response

from rest_framework import permissions
from django.contrib.auth.models import User

# login lib
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login

# my files
from . import models
from . import serializers
from . import premissions
from . import filters


# Create your views here.
def api(request):
    return JsonResponse(
        {"message": "Hello, this is zkaria portfolio api v2"}, status=200
    )


# login user
class UserLogin(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    permission_classes = [premissions.onlyUnAuth]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            user_data = {
                "token": token.key,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "is_superuser": user.is_superuser,
                    "isAuthenticated": user.is_authenticated,
                },
                "is_superuser": user.is_superuser,
            }
            return response.Response(user_data)
        else:
            return response.Response({"error": "Invalid credentials"})


# create user
class UserRegisteration(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.Registration
    permission_classes = [premissions.onlyUnAuth]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get("password"))
            user.save()
            return response.Response({"success": True, "message": "user Created"})
        return response.Response({"success": False, "message": "Registration failed"})


# create post or see all posts
class ProjectPostView(
    mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView
):
    queryset = models.ProjectPost.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [premissions.SuperOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.PostFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# edit and delete post
class ProjectPostViewDetail(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    generics.GenericAPIView,
):
    queryset = models.ProjectPost.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [premissions.SuperOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # this is update function
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    # this is delete function
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# call all tags
class allTags(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.Tags.objects.all()
    serializer_class = serializers.TagsSerializer
    permission_classes = [premissions.SuperOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# get all comments
class CommentSection(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = models.post_comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Retrieve the post ID from the URL parameters
        post_id = self.kwargs["post_id"]
        # Filter comments by the post ID
        queryset = models.post_comment.objects.filter(post=post_id)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        return self.create(request, *args, **kwargs)


# to get specific user
class ProfileUser(mixins.ListModelMixin, generics.GenericAPIView):
    def get_queryset(self):
        # Retrieve the post ID from the URL parameters
        user_id = self.kwargs["user_id"]
        # Filter comments by the post ID
        queryset = models.Profile.objects.filter(user=user_id)
        return queryset

    serializer_class = serializers.ProfileSerializer
    permission_classes = [premissions.SuperOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class NotifyUser(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = models.notify_user.objects.all()
    serializer_class = serializers.notifySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class createNotifyUser(
    mixins.CreateModelMixin, generics.GenericAPIView, mixins.ListModelMixin
):
    serializer_class = serializers.notifySerializer
    queryset = models.notify_user.objects.all()
    permission_classes = [premissions.SuperUserOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class getResume(
    generics.GenericAPIView,
    mixins.ListModelMixin,
):
    queryset = models.my_resume.objects.all()
    serializer_class = serializers.my_resumeSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        if serializer.data:
            resume_link = serializer.data[0]["resume"]
            return response.Response({"file": resume_link})
        return response.Response({"file": None})
