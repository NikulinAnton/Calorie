import datetime

import requests
from django.contrib.auth import login, logout
from django.db.models import Prefetch, Sum
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from calories import settings
from core.models import Diet, DietFood
from core.permissions import IsSuperuserOrIsObjectOwner
from core.serializers import (
    DayIncomeCaloriesSerializer,
    DayIncomeMacronutrientsSerializer,
    DietFoodSerializer,
    DietListSerializer,
    DietSerializer,
    FoodReadOnlySerializer,
    LoginSerializer,
)
from core.utils import get_day_calories, get_day_macronutrients


class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    @extend_schema(responses={200: ""})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        keep_logged_in = serializer.validated_data["keep_logged_in"]
        login(request, user)
        if not keep_logged_in:
            request.session.set_expiry(0)
        return Response()


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        logout(request)
        return Response()


class FoodView(APIView):
    @extend_schema(
        parameters=[OpenApiParameter("name", OpenApiTypes.STR, OpenApiParameter.QUERY)]
    )
    def get(self, request):
        nutrition_api_url = f"https://api.api-ninjas.com/v1/nutrition?query={self.request.query_params.get('name')}"
        response_data = requests.get(
            nutrition_api_url, headers={"X-Api-Key": settings.NUTRITION_API_KEY}
        ).json()
        serializer = FoodReadOnlySerializer(data=response_data, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DietViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    serializer_class = DietSerializer
    permission_classes = [IsSuperuserOrIsObjectOwner]
    queryset = Diet.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return DietListSerializer
        if self.action == "day_calories":
            return DayIncomeCaloriesSerializer
        if self.action == "day_macronutrients":
            return DayIncomeMacronutrientsSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action != "list":
            queryset = queryset.prefetch_related(
                Prefetch("diet_foods", DietFood.objects.select_related("diet", "food"))
            )
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(owner=self.request.user)

    @extend_schema(
        parameters=[OpenApiParameter("date", OpenApiTypes.DATE, OpenApiParameter.QUERY)]
    )
    @action(detail=False, methods=["GET"], url_path="day-calories")
    def day_calories(self, request, *args, **kwargs):
        owner = self.request.user
        date = self.request.query_params.get("date", datetime.date.today())
        day_calories = get_day_calories(owner=owner, date=date)
        serializer = self.get_serializer(day_calories)
        return Response(serializer.data)

    @extend_schema(
        parameters=[OpenApiParameter("date", OpenApiTypes.DATE, OpenApiParameter.QUERY)]
    )
    @action(detail=False, methods=["GET"], url_path="day-macronutrients")
    def day_macronutrients(self, request, *args, **kwargs):
        owner = self.request.user
        date = self.request.query_params.get("date", datetime.date.today())
        day_macronutrients = get_day_macronutrients(owner=owner, date=date)
        serializer = self.get_serializer(day_macronutrients)
        return Response(serializer.data)


class DietFoodViewSet(ModelViewSet):
    serializer_class = DietFoodSerializer
    permission_classes = [IsSuperuserOrIsObjectOwner]
    queryset = DietFood.objects.select_related("diet", "food")

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(owner=self.request.user)
