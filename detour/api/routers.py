from rest_framework.routers import Route, DynamicRoute, SimpleRouter

class PathRouter(SimpleRouter):
    """
    A router for read-only APIs, which doesn't use trailing slashes.
    """
    routes = [
        DynamicRoute(
            url=r'^{prefix}/{url_path}/{lookup}\.csv$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        )
    ]
