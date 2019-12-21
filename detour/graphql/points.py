from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from detour.api.models import Point


class PointNode(DjangoObjectType):
    class Meta:
        model = Point
        filter_fields = ["trip"]
        interfaces = (relay.Node,)


class Query(ObjectType):
    point = relay.Node.Field(PointNode)
    points = DjangoFilterConnectionField(PointNode)
