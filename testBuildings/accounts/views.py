from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView


class AccountLoginView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        print request.data
        return Response("ok", status=200)
