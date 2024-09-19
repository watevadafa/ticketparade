from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from ticketparade.users.api.views import (
    UserViewSet,
    TheaterSeatsViewSet,
    TheaterViewSet,
)

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("theaters", TheaterViewSet)
router.register("theater-seats", TheaterSeatsViewSet)


app_name = "api"
urlpatterns = router.urls
