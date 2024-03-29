from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_csv.parsers import CSVParser
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from itertools import accumulate
from haversine import haversine
from .permissions import IsOwnerOrReadOnly
from .serializers import PointSerializer, TripSerializer
from .models import Point, Trip
from .negotiation import IgnoreClientContentNegotiation


class PointViewSet(viewsets.ModelViewSet):
    """
    Point view
    """

    serializer_class = PointSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("annotation",)

    def get_queryset(self):
        return Point.objects.filter(trip=self.kwargs["trip_pk"])


class TripViewSet(viewsets.ModelViewSet):
    """
    Point view
    """

    queryset = Trip.objects.all().order_by("-created_at")
    serializer_class = TripSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    @action(methods=["GET"], detail=True)
    def linestring(self, request, pk=None):
        """Return a GeoJSON linestring of this trip"""
        trip = Trip.objects.get(pk=pk)
        points = trip.points.values("lat", "lon").all().order_by("time")

        return Response(
            {"type": "LineString", "coordinates": points.values_list("lon", "lat")}
        )

    @action(methods=["GET"], detail=True)
    def distance(self, request, pk=None):
        """Return cumulative distance as a function of time"""
        trip = Trip.objects.get(pk=pk)
        distances = trip.distance()

        return Response({"distance": distances})

    @action(methods=["GET"], detail=True)
    def speed(self, request, pk=None):
        """Returns speed as a function of time"""
        trip = Trip.objects.get(pk=pk)
        points = trip.points.values("time", "speed").all().order_by("time")

        speed = [
            [int(v[0].timestamp()), v[1] * 60 * 60 / 1000]
            for v in points.values_list("time", "speed")
        ]
        return Response({"speed": speed}, 200)

    @action(methods=["GET"], detail=True)
    def annotations(self, request, pk=None):
        """Returns annotation points"""
        trip = Trip.objects.get(pk=pk)
        points = (
            trip.points.filter(annotation__isnull=False)
            .exclude(annotation__exact="")
            .all()
            .order_by("time")
        )

        return Response(
            {"annotations": points.values_list("time", "lat", "lon", "annotation")}, 200
        )


class UploadView(APIView):
    serializer_class = PointSerializer
    content_negotiation_class = IgnoreClientContentNegotiation
    parser_classes = [CSVParser]
    renderer_classes = [JSONRenderer]
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def put(self, request, pk=None, trip_id=None):
        """
        Receives a csv file containing point data and inserts into database.
        """
        success = 0
        errors = []
        for point in request.data:
            point["trip"] = trip_id
            serializer = self.serializer_class(data=point, many=False)
            if serializer.is_valid():
                serializer.save()
                success += 1
            else:
                errors.append(serializer.errors)

        return Response({"message": f"Added {success} points", "errors": errors}, 201)
