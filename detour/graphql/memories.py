from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from detour.api.models import Memory


class MemoryNode(DjangoObjectType):
    class Meta:
        model = Memory
        filter_fields = ["trip"]
        interfaces = (relay.Node,)


class Query(ObjectType):
    memory = relay.Node.Field(MemoryNode)
    memories = DjangoFilterConnectionField(MemoryNode)

    def resolve_posts(self, info, trip):
        _, trip_id = from_global_id(trip)
        return Memory.objects.filter(trip__id=trip_id).all()
