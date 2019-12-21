from graphene import relay, ObjectType, Field, List, String, Int
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from detour.api.models import Trip


class Geometry(ObjectType):
    type = String(default_value="LineString")
    coordinates = List(List(Int))


class GeoJSON(ObjectType):
    type = String(default_value="Feature")
    geometry = Field(Geometry)


class TripNode(DjangoObjectType):
    class Meta:
        model = Trip
        filter_fields = ["name"]
        interfaces = (relay.Node,)

    geoJSON = Field(GeoJSON)

    def resolve_geoJSON(self, info, **kwargs):

        coordinates = self.points.values("lat", "lon").order_by("time").all()

        return GeoJSON(
            geometry=Geometry(coordinates=coordinates.values_list("lon", "lat"))
        )


class Query(ObjectType):
    trip = relay.Node.Field(TripNode)
    trips = DjangoFilterConnectionField(TripNode)
