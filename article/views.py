from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from article.serializers import ArticleSerializers
from article.models import Article
from user.models import User
from user.permissions import UserPermission
from rest_framework.request import QueryDict
# Create your views here.


class APIArticle(ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializers
    permission_classes = (UserPermission, )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if data['type'] == "PRIVATE":
            if not request.user.is_authenticated:
                return Response("You must be Follower", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if not request.user.is_authenticated:
            queryset = queryset.filter(type="PUBLIC")

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            article = serializer.create(validated_data=serializer.validated_data)
            return Response(ArticleSerializers(article).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


