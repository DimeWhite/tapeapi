from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.views import *
app_name = 'user'

router = DefaultRouter()
router.register('user', APIUser)

urlpatterns = [
    path('user/', include(router.urls)),
]