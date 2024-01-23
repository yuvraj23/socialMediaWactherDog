
from django.urls import path,include
from account.views import UserRegistrationView,UserLoginView,ProfileView,UserChangePasswordView,\
    YoutubeConfigCreate,YoutubeMetricsView,UserYoutubeAllChannel

urlpatterns=[
    path("register/",UserRegistrationView.as_view(),name="register"),
    path("login/",UserLoginView.as_view(),name="login"),
    path("profile/",ProfileView.as_view(),name="profile"),
    path("change_password/",UserChangePasswordView.as_view(),name="change_password"),
     path('youtube-config/create/', YoutubeConfigCreate.as_view(), name='youtube-config-create'),
    path('youtube_metrics/', YoutubeMetricsView.as_view(), name='youtube_metrics'),
    path('youtube_list/', UserYoutubeAllChannel.as_view(), name='youtube_list'),

    #  path("logout/",LogoutView.as_view(),name="logout"),
]