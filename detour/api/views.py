from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_csv.parsers import CSVParser
from rest_framework.renderers import JSONRenderer
from .serializers import PointSerializer
from .models import Point
from .negotiation import IgnoreClientContentNegotiation


class PointViewSet(viewsets.ModelViewSet):
    """
    Point view
    """
    queryset = Point.objects.all().order_by('-created_at')
    serializer_class = PointSerializer


class UploadView(APIView):
    serializer_class = PointSerializer
    content_negotiation_class = IgnoreClientContentNegotiation
    parser_classes = [CSVParser]
    renderer_classes = [JSONRenderer]

    def put(self, request, pk=None, trip_id=None):
        """
        Receives a csv file containing point data and inserts into database.
        """
        points = []
        for point in request.data:
            point['trip'] = trip_id
            points.append(point)

        serializer = self.serializer_class(data=points, many=True)
        valid = serializer.is_valid()

        if valid:
            serializer.save()
            return Response({'message': f'Added {len(serializer.data)} points'},
                            201)
        else:
            return Response(serializer.errors, 400)
