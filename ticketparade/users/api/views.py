from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action

from core.utils import get_popular_movies


from ticketparade.users.models import User, Theater, TheaterSeat

from .serializers import (
    UserSerializer,
    TheaterSerialzer,
    TheaterSeatSerializer,
    MovieSerialzer,
    BookTheaterSeatSerialzer,
)


class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "pk"

    def get_queryset(self, *args, **kwargs):
        assert isinstance(self.request.user.id, int)
        return self.queryset.filter(id=self.request.user.id)


class TheaterViewSet(ReadOnlyModelViewSet):
    serializer_class = TheaterSerialzer
    queryset = Theater.objects.all().select_related("seats")
    lookup_field = "pk"

    @action(detail=True)
    def get_movies(self, request, *args, **kwargs):
        movies = get_popular_movies()
        serializer = MovieSerialzer(movies, many=True)
        return Response(serializer.data)


class TheaterSeatsViewSet(ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    queryset = Theater.objects.all().select_related("seats")
    lookup_field = "pk"
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_fields = ["theater", "is_available"]

    @action(detail=False)
    def book(self, request, *args, **kwargs):
        data = request.data
        serializer = BookTheaterSeatSerialzer(data=data)
        return Response(serializer.data)
