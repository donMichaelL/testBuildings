from django.shortcuts import render, get_object_or_404
from django.core import exceptions
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .serializers import BuildingSerializer, FloorSerializer
from .models import Building, Floor


class BuildingListView(ListCreateAPIView):
    serializer_class = BuildingSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Building.objects.all()
        return Building.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.pk
        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception, err:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuildingDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = BuildingSerializer
    queryset = Building.objects.all();
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = super(BuildingDetailView, self).get_object()
        if obj.user == self.request.user or self.request.user.is_superuser:
            return obj
        raise exceptions.PermissionDenied()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy().dict()
        for key, value in data.items():
            if value == 'null':
                data[key] = None
        if 'photo' in data and type(data['photo']) is unicode:
            data.pop('photo')
        try:
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception, err:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FloorListView(ListCreateAPIView):
    serializer_class = FloorSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        building = get_object_or_404(Building, pk=self.kwargs.get('pk_building'))
        if building.user == self.request.user or self.request.user.is_superuser:
            return Floor.objects.filter(building=building)
        raise exceptions.PermissionDenied()

    def post(self, request, *args, **kwargs):
        if ('blueprint' not in request.data) or (request.data['blueprint'] == None):
            raise serializers.ValidationError({'blueprint': 'No file was submitted.'})
        return self.create(request, *args, **kwargs)

class FloorDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = FloorSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        building = get_object_or_404(Building, pk=self.kwargs.get('pk_building'))
        if building.user == self.request.user or self.request.user.is_superuser:
            return Floor.objects.filter(building=building)
        raise exceptions.PermissionDenied()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy().dict()
        for key, value in data.items():
            if value == 'null':
                data[key] = None
        if 'blueprint' not in data or  data['blueprint'] == None:
            raise serializers.ValidationError({'blueprint': 'No file was submitted.'})
        if type(data['blueprint']) is unicode:
            data.pop('blueprint')
        try:
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception, err:
            print err
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
