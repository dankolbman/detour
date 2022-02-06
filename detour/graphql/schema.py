import graphene
from .points import Query as PointQuery
from .trips import Query as TripQuery
from .memories import Query as MemoryQuery
from .posts import Query as PostQuery


class Query(TripQuery, MemoryQuery, PointQuery, PostQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
