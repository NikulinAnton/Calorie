from django.contrib.auth import authenticate
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated, ValidationError

from core.models import Diet, DietFood, Food
from core.utils import create_dietfood, update_dietfood


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    keep_logged_in = serializers.BooleanField(default=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(email=email, password=password)

        if not user:
            raise NotAuthenticated(
                "Unable to log in with provided credentials.", "authorization"
            )

        attrs["user"] = user
        return attrs


class FoodReadOnlySerializer(serializers.Serializer):
    name = serializers.CharField()
    calories = serializers.FloatField()
    protein_g = serializers.FloatField()
    carbohydrates_total_g = serializers.FloatField()
    fat_total_g = serializers.FloatField()


class FoodWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["name", "calories", "proteins", "carbs", "fats"]


class DietFoodSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(default=1, min_value=1, max_value=2147483647)
    food = FoodWriteSerializer()

    class Meta:
        model = DietFood
        fields = ["id", "diet", "food", "quantity"]

    @transaction.atomic()
    def create(self, validated_data):
        return create_dietfood(validated_data, self.context["request"].user)

    def update(self, instance, validated_data):
        return update_dietfood(instance, validated_data, self.context["request"].user)


class DietSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diet
        fields = ["id", "owner", "date"]
        read_only_fields = ["id", "owner"]

    def validate_date(self, date):
        queryset = Diet.objects.filter(owner=self.context["request"].user, date=date)
        if queryset.exists():
            raise ValidationError(
                f"Current user already has diet for the date: {date.strftime('%d.%m.%Y')}"
            )
        return date

    def create(self, validated_data):
        instance = super().create(
            {**validated_data, "owner": self.context["request"].user}
        )
        return instance
