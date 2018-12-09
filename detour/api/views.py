from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_csv.parsers import CSVParser
from rest_framework.renderers import JSONRenderer
from .serializers import PointSerializer, TripSerializer
from .models import Point, Trip
from .negotiation import IgnoreClientContentNegotiation


class PointViewSet(viewsets.ModelViewSet):
    """
    Point view
    """
    serializer_class = PointSerializer

    def get_queryset(self):
        return Point.objects.filter(trip=self.kwargs['trip_pk'])


class TripViewSet(viewsets.ModelViewSet):
    """
    Point view
    """
    queryset = Trip.objects.all().order_by('-created_at')
    serializer_class = TripSerializer


class UploadView(APIView):
    serializer_class = PointSerializer
    content_negotiation_class = IgnoreClientContentNegotiation
    parser_classes = [CSVParser]
    renderer_classes = [JSONRenderer]

    def put(self, request, pk=None, trip_id=None):
        """
        Receives a csv file containing point data and inserts into database.
        """
        success = 0
        errors = []
        for point in request.data:
            point['trip'] = trip_id
            serializer = self.serializer_class(data=point, many=False)
            if serializer.is_valid():
                serializer.save()
                success += 1
            else:
                errors.append(serializer.errors)

        return Response({'message': f'Added {success} points',
                         'errors': errors},
                        201)
