from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Story
from .serializers import StorySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class StoriesAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.GET.get('pk'):
            story = get_object_or_404(Story, pk=request.GET.get('pk'))
            serializer = StorySerializer(story)
            return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)
        else:
            app_categories = Story.objects.all()
            serializer = StorySerializer(app_categories, many=True)
            return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StorySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            story = Story.objects.filter(created_by = request.user)
            serializer = StorySerializer(story, many=True)
            return Response({"success":True, 'details': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success":False, 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 

    # def put(self, request):
    #     story = get_object_or_404(Story, pk=request.data.get('id'), created_by= request.user)
    #     serializer = StorySerializer(story, data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)
    #     return Response({"success":False, 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        validated_data= {
            'content': request.data.get('content')
        }
        story = get_object_or_404(Story, pk=request.data.get('id'))
        serializer = StorySerializer(story, data=validated_data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"success":True, 'details': serializer.data}, status=status.HTTP_200_OK)
        return Response({"success":False, 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        story = get_object_or_404(Story, pk=request.GET.get('pk'), created_by= request.user)
        story.delete()
        return Response({"success":True, 'details': "Deleted Successfully"}, status=status.HTTP_200_OK)
    