from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import RegisterUserSerializer, UserSerializer
from .models import User


class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Вы успешно зарегистрировались', status=201)


@api_view(['DELETE'])
def delete(request, email):
    user = get_object_or_404(User, email=email)
    if user.is_staff:
        return Response(status=403) # запрещаем
    user.delete()
    return Response('Успешно удалили акаунт', status=204)


@api_view(['GET'])
def activate_view(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True # activate user
    user.activation_code = '' # delete the activated code
    user.save()
    return Response('Successfuly activated the account', 200)

@api_view(['GET'])
def user_detail(request, id):
    user = get_object_or_404(User, id=id)
    return Response(UserSerializer(user).data, status=200)

