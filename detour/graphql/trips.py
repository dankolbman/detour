from graphene import relay, ObjectType, Field, List, String, Float, DateTime
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from detour.api.models import Trip


class TimePoint(ObjectType):
    time = DateTime()
    value = Float()


class Geometry(ObjectType):
    type = String(default_value="LineString")
    coordinates = List(List(Float))


class GeoJSON(ObjectType):
    type = String(default_value="Feature")
    geometry = Field(Geometry)


class TripNode(DjangoObjectType):
    class Meta:
        model = Trip
        filter_fields = ["name"]
        interfaces = (relay.Node,)

    geoJSON = Field(GeoJSON)
    distance = List(TimePoint)

    def resolve_geoJSON(self, info, **kwargs):

        coordinates = self.points.values("lat", "lon").order_by("time").all()

        return GeoJSON(
            geometry=Geometry(coordinates=coordinates.values_list("lon", "lat"))
        )

    def resolve_distance(self, info, **kwargs):
        distances = self.distance(resolution=100)
        d = [TimePoint(time=p["time"], value=p["distance"]) for p in distances]
        return d


class Query(ObjectType):
    trip = relay.Node.Field(TripNode)
    trips = DjangoFilterConnectionField(TripNode)

    def resolve_trips(self, *args, **kwargs):
        return Trip.objects.filter(visible=True).all()
