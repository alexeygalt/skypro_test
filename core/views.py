from django.contrib.auth import get_user_model, logout
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response

from core.serializers import UserSerializer, UserLoginSerializer

USER_MODEL = get_user_model()


class ListCreateUserView(ListCreateAPIView):
    model = USER_MODEL
    queryset = model.objects.all()
    serializer_class = UserSerializer


class RetrieveDestroyUserView(RetrieveDestroyAPIView):
    model = USER_MODEL
    queryset = model.objects.all()
    serializer_class = UserSerializer


class UserLogin(CreateAPIView):
    model = USER_MODEL
    serializer_class = UserLoginSerializer


class UserLogout(GenericAPIView):
    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status.HTTP_200_OK)
