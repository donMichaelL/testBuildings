from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


class AccountLoginView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user.is_active:
            login(request, user)
            return Response('Logged In', status=200)
        else:
            return Response("Error", status=401)


class AccountLogoutView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        print 'here i am'
        logout(request)
        return Response('Loggout Out', status=200)
