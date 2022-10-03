from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from core import views

router = routers.DefaultRouter()
router.register("diets", views.DietViewSet, basename="diet")
router.register("dietfoods", views.DietFoodViewSet, basename="dietfood")


schema_views = [
    path("", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="schema_swagger",
    ),
    path(
        "redoc/", SpectacularRedocView.as_view(url_name="schema"), name="schema_redoc"
    ),
    path("json/", SpectacularJSONAPIView.as_view(), name="schema_json"),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(router.urls)),
    path("api/v1/login/", views.LoginView.as_view(), name="login"),
    path("api/v1/logout/", views.LogoutView.as_view(), name="logout"),
    path("api/v1/foods/", views.FoodView.as_view(), name="food"),
    path("schema/", include(schema_views)),
]
