from django.shortcuts import render , HttpResponse

# filter lib
from django_filters.rest_framework import DjangoFilterBackend
# restframework lib
from rest_framework import mixins , generics , response

# from rest_framework import permissions
from django.contrib.auth.models import User

# login lib
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login

# my files 
from .models import *
from .serializers import *
from .premissions import *
from .filters import *

# Create your views here.
def api(request):
    return HttpResponse('lol')


# login user
class UserLogin(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [onlyUnAuth]
    def post(self , request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request , username = username , password = password)

        if user:
            login(request , user)
            token, _ = Token.objects.get_or_create(user=user)
            user_data = {
                'token': token.key,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email':user.email,
                    'is_superuser':user.is_superuser,
                    'isAuthenticated':user.is_authenticated
                },
                'is_superuser': user.is_superuser
            }
            return response.Response(user_data)
        else:
            return response.Response({'error': 'Invalid credentials'})
        
# create user 
class UserRegisteration(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = Registration
    permission_classes = [onlyUnAuth]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(request.data.get('password'))
            user.save()
            return response.Response({'success': True , 'message':'user Created'})
        return response.Response({'success': False, 'message': 'Registration failed'})

# create post or see all posts
class ProjectPostView(mixins.CreateModelMixin , 
                  mixins.ListModelMixin ,
                  generics.GenericAPIView):
    queryset = ProjectPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [SuperOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class  = PostFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# edit and delete post
class ProjectPostViewDetail(mixins.RetrieveModelMixin , 
                  mixins.DestroyModelMixin ,
                  mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    queryset = ProjectPost.objects.all()
    serializer_class = PostSerializer
    permission_classes = [SuperOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    # this is update function
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    # this is delete function
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

# call all tags
class allTags(mixins.CreateModelMixin,
              mixins.ListModelMixin,
              generics.GenericAPIView):
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = [SuperOrReadOnly]

    def get(self , request , *args , **kwargs):
        return self.list(request , *args ,**kwargs)
    def post(self , request , *args , **kwargs):
        return self.create(request , *args ,**kwargs)

# get all comments
class CommentSection(mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     generics.GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Retrieve the post ID from the URL parameters
        post_id = self.kwargs['post_id']
        # Filter comments by the post ID
        queryset = post_comment.objects.filter(post=post_id)
        return queryset

    def get(self , request , *args , **kwargs):
        return self.list(request , *args ,**kwargs)
    
    def post(self , request , *args , **kwargs):

        return self.create(request , *args ,**kwargs) 

# to get specific user
class ProfileUser(mixins.ListModelMixin ,
                  generics.GenericAPIView):
    def get_queryset(self):
        # Retrieve the post ID from the URL parameters
        user_id = self.kwargs['user_id']
        # Filter comments by the post ID
        queryset = Profile.objects.filter(user=user_id)
        return queryset
    serializer_class = ProfileSerializer
    permission_classes = [SuperOrReadOnly]
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class NotifyUser(mixins.ListModelMixin ,
                  generics.GenericAPIView):
    queryset= notify_user.objects.all()
    serializer_class = notifySerializer
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class createNotifyUser(mixins.CreateModelMixin,
                        generics.GenericAPIView,
                        mixins.ListModelMixin):
    serializer_class = notifySerializer
    queryset= notify_user.objects.all()
    permission_classes = [SuperUserOnly]
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self , request , *args , **kwargs):
        return self.create(request , *args ,**kwargs)
