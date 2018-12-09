from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from rest_framework import routers
from .api import views
from .api.routers import PathRouter

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'points', views.PointViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    path('remote.php/webdav/<int:trip_id>/<str:pk>',
         views.UploadView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
