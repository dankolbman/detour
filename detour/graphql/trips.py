from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from detour.api.models import Trip


class TripNode(DjangoObjectType):
    class Meta:
        model = Trip
        filter_fields = ["name"]
        interfaces = (relay.Node,)


class Query(ObjectType):
    trip = relay.Node.Field(TripNode)
    trips = DjangoFilterConnectionField(TripNode)
