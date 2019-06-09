# Detour

A simple Django app for storing and providing GPS traces for crazy adventures.

## Developing

Start up detour with docker-compose:
```
docker-compose up
```

This will start up the api in a container on port `5000` with the repository mounted and the django development server running.
If database models are change through an addition of a migration, the detour container will need to be restarted or run:
```
docker-compose exec detour ./manage.py migrate
```

## Testing

With docker-compose services running, tests may be run with:
```
docker-compose exec detour pytest
```
