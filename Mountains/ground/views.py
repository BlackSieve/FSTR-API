from django.shortcuts import render
from rest_framework import viewsets
from .models import LevelPoint, Image, User, Coord, StatusAdd
from .serializers import ImageSerializer, CoordSerializer, UserSerializer, LevelPointSerializer


class UserAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CoordAPIView(viewsets.ModelViewSet):
    queryset = Coord.objects.all()
    serializer_class = CoordSerializer


class LevelAPIView(viewsets.ModelViewSet):
    queryset = LevelPoint.objects.all()
    serializer_class = LevelPointSerializer


class ImageAPIView(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
