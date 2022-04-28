from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication, permissions
from user.models import User
from user.serializers import *
from rest_framework.permissions import IsAdminUser


class APIUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser, ]

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.create(validated_data=serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response({"errors": serializer.errors})
