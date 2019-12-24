from graphene import relay, ObjectType, Field, List, String, Float, DateTime
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay import from_global_id

from detour.api.models import Post
from .trips import TimePoint


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = ["author", "trip"]
        interfaces = (relay.Node,)



class Query(ObjectType):
    post = relay.Node.Field(PostNode)
    posts = DjangoFilterConnectionField(PostNode)

    def resolve_posts(self, info, trip):
        _, trip_id = from_global_id(trip)
        return Post.objects.filter(trip__id=trip_id).all()
