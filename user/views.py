from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from user.models import User
from user.serializers import UserSerializer, UserAuthorizationSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework import status


class APIUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAdminUser, ]
    serializers = {
        'list': UserSerializer,
        'retrieve': UserSerializer,
        'authorization': UserAuthorizationSerializer
    }

    @action(detail=False, methods=["GET"])
    def logout(self, request):
        logout(request)
        return Response({'logout': True})

    @action(detail=False, methods=["POST"])
    def authorization(self, request):
        serializer = UserAuthorizationSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = authenticate(email=data['email'],
                                password=data['password'], )
            if user:
                login(request, user)
                return Response({'success': True,
                                 'user': UserSerializer(User.objects.get(email=user.email)).data})
            else:
                return Response({'success': False})
        else:
            return Response({'error': serializer.errors})

    def create(self, request, *args, **kwargs):
        if request.user.is_superuser or True:
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                serializer.create(validated_data=serializer.validated_data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'You must be admin'})

    def get_serializer_class(self):
        for i in list(self.serializers.keys()):
            return self.serializers.get(self.action,
                                        self.serializers[i])
