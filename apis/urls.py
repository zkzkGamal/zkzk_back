from django.urls import path
from . import views

urlpatterns = [
    path("", views.api, name="important"),
    path("posts", views.ProjectPostView.as_view(), name="allProject"),
    path("posts/<int:pk>", views.ProjectPostViewDetail.as_view(), name="projectDetail"),
    path("registeration/register", views.UserRegisteration.as_view(), name="singUP"),
    path("registeration/login", views.UserLogin.as_view(), name="Login"),
    path("tags", views.allTags.as_view(), name="tags"),
    path("comment/<int:post_id>", views.CommentSection.as_view(), name="comments"),
    path(
        "ProfileDetail/<int:user_id>", views.ProfileUser.as_view(), name="profileUser"
    ),
    path("notifications", views.NotifyUser.as_view(), name="notification"),
    path(
        "notifications/create", views.createNotifyUser.as_view(), name="create_notify"
    ),
    path("resume", views.getResume.as_view(), name="resume"),
]
