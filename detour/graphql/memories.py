from django_filters import FilterSet, OrderingFilter
from graphene import relay, ObjectType, String
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from detour.api.models import Memory


class MemoryFilter(FilterSet):
    class Meta:
        model = Memory
        fields = ("trip", "time")

    order_by = OrderingFilter(
        fields=(
            "created_at",
            "time",
        )
    )


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
