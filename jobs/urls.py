from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    JobOfferViewSet,
    JobSearchQueryViewSet,
    RunFetchView,
    TranslateView,
)

router = DefaultRouter()
router.register(r"offers", JobOfferViewSet, basename="job-offer")
router.register(r"queries", JobSearchQueryViewSet, basename="job-query")

urlpatterns = [
    path("fetch/", RunFetchView.as_view(), name="job-fetch"),
    path("translate/", TranslateView.as_view(), name="job-translate"),
    path("", include(router.urls)),
]
