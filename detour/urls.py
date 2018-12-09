from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from rest_framework_nested import routers
from .api import views
from .api.routers import PathRouter

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'trips', views.TripViewSet)

trip_router = routers.NestedSimpleRouter(router, r'trips', lookup='trip')
trip_router.register(r'points', views.PointViewSet, basename='trip-points')

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(trip_router.urls)),
    path('remote.php/webdav/<int:trip_id>/<str:pk>',
         views.UploadView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
