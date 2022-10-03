import requests
from django.contrib.auth import login, logout
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from calories import settings
from core.models import Diet, DietFood
from core.permissions import IsSuperuserOrIsObjectOwner
from core.serializers import (
    DietFoodSerializer,
    DietSerializer,
    FoodReadOnlySerializer,
    LoginSerializer,
)


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


class DietFoodViewSet(ModelViewSet):
    serializer_class = DietFoodSerializer
    permission_classes = [IsSuperuserOrIsObjectOwner]
    queryset = DietFood.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return queryset
        return queryset.filter(owner=self.request.user)
