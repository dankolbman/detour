from django.conf.urls import url, include
from rest_framework import routers
from .api import views
from .api.routers import PathRouter

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'points', views.PointViewSet)

p_router = PathRouter()
p_router.register(r'webdav', views.BulkPointViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^remote.php/', include(p_router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
