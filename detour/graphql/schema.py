import graphene
from .points import Query as PointQuery
from .trips import Query as TripQuery


class Query(TripQuery, PointQuery, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
