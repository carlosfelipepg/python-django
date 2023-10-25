from django.urls import path
from link.views import LinkAPIView

urlpatterns = [
    path("link/", LinkAPIView.as_view(), name="link-api"),
    path("link/<str:token>/", LinkAPIView.as_view(), name="link-api-token"),
]
