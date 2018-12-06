import csv
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_csv.parsers import CSVParser
from .serializers import PointSerializer
from .models import Point


class PointViewSet(viewsets.ModelViewSet):
    """
    Point view
    """
    queryset = Point.objects.all().order_by('-created_at')
    serializer_class = PointSerializer


class BulkPointViewSet(viewsets.ModelViewSet):
    """
    View for uploading a csv file containing points
    """
    queryset = Point.objects.all().order_by('-created_at')
    serializer_class = PointSerializer
    parser_classes = (CSVParser,)

    @action(detail=True, methods=['put'], name='Upload')
    def points(self, request, pk=None):
        """
        Receives a csv file containing point data and inserts into database.
        """
        serializer = self.get_serializer(data=request.data, many=True)
        valid = serializer.is_valid()
        if valid:
            serializer.save()
            return Response({'message': f'Added {len(serializer.data)} points'})
        else:
            return Response(serializer.errors, 400)
