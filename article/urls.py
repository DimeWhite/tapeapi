from django.urls import path, include
from rest_framework.routers import DefaultRouter
from article.views import *
app_name = 'article'

router = DefaultRouter()
router.register('article', APIArticle)

urlpatterns = [
    path('article/', include(router.urls))
]