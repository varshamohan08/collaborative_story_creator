from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.contrib.auth.models import User
from .serializers import UserSerializer


class userLogin(APIView):

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            user_serializer = UserSerializer(user)
            return Response(
                {
                    'status': True,
                    'user': user_serializer.data,
                    'access_token': access_token
                }, 
                status=status.HTTP_200_OK
            )

        return Response(
            {
                'status': False,
                'errors': 'Invalid credentials'
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )


class userLogout(APIView):
    def get(self, request):
        logout(request)
        return Response({'details': 'Success'}, status=status.HTTP_200_OK)


class userSignUp(APIView):
    def post(self, request):
        import pdb;pdb.set_trace()
        with transaction.atomic():
            user_serializer = UserSerializer(data=request.data)

            if user_serializer.is_valid():
                user_serializer.save()
                user = authenticate(
                    username=request.data.get('username'),
                    password=request.data.get('password')
                )

                if user:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    return Response(
                        {
                            'status': True,
                            'user': user_serializer.data,
                            'access_token': access_token
                        }, 
                        status=status.HTTP_200_OK
                    )

            return Response(
                {
                    'status': False,
                    'errors': user_serializer.errors
                }, 
                status=status.HTTP_400_BAD_REQUEST
            )


class userApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # import pdb;pdb.set_trace()
        user_instance = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user_instance)
        return Response({'status': True, 'user': serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request):
        with transaction.atomic():
            User.objects.filter(id=request.user.id).delete()
            logout(request)
            return Response({'status': True}, status=status.HTTP_200_OK)