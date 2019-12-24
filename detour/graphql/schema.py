import graphene
from .points import Query as PointQuery
from .trips import Query as TripQuery
from .posts import Query as PostQuery


class Query(TripQuery, PointQuery, PostQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
