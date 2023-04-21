from django.urls import path

from core.views import ListCreateUserView, RetrieveDestroyUserView, UserLogin, UserLogout

urlpatterns = [
    path("", ListCreateUserView.as_view()),
    path("<int:pk>/", RetrieveDestroyUserView.as_view()),
    path("login/", UserLogin.as_view()),
    path("logout/", UserLogout.as_view()),
]
