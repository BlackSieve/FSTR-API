"""
URL configuration for Mountains project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from ground.views import StatusAPIView, ImageAPIView,UserAPIView,LevelAPIView,CoordAPIView

router = routers.DefaultRouter()
router.register(r'submitdata', StatusAPIView)

"""
Ниже в комментарии приведены роутеры, для работы с каждым APIView по отдельности
"""
# router.register(r'user', UserAPIView)
# router.register(r'image', ImageAPIView)
# router.register(r'level', LevelAPIView)
# router.register(r'coord', CoordAPIView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]