import collections

from django_tiny_util.models import update_fields
from rest_framework.generics import get_object_or_404

from core.models import CUser, Diet, DietFood, Food


def create_diet_food(validated_data: dict, owner: CUser) -> DietFood:
    food_data = validated_data.pop("food")
    food = _update_or_create_food(food_data, owner)
    return DietFood.objects.create(**validated_data, food=food)


def update_diet_food(
    diet_food_instance: DietFood, validated_data: dict, owner: CUser
) -> DietFood:
    food_data = validated_data.pop("food")
    food, _ = _update_or_create_food(food_data, owner)
    update_fields(diet_food_instance, food=food)
    return diet_food_instance


def _update_or_create_food(food_data: collections.OrderedDict, owner: CUser) -> Food:
    food, _ = Food.objects.update_or_create(
        name=food_data.get("name"),
        owner=owner,
        defaults=dict(
            calories=food_data.get("calories"),
            proteins=food_data.get("proteins"),
            carbs=food_data.get("carbs"),
            fats=food_data.get("fats"),
        ),
    )
    return food


def get_day_calories(owner: CUser, date: str) -> dict:
    diet = get_object_or_404(Diet, owner=owner, date=date)
    total_calories = 0
    for diet_food in diet.diet_foods.all():
        total_calories += diet_food.quantity * diet_food.food.calories / 100
    return dict(total_calories=total_calories or 0)


def get_day_macronutrients(owner: CUser, date: str) -> dict:
    diet = get_object_or_404(Diet, owner=owner, date=date)
    total_proteins = 0
    total_carbs = 0
    total_fats = 0
    for diet_food in diet.diet_foods.all():
        total_proteins += diet_food.quantity * diet_food.food.proteins / 100
        total_carbs += diet_food.quantity * diet_food.food.carbs / 100
        total_fats += diet_food.quantity * diet_food.food.fats / 100
    return dict(
        total_proteins=total_proteins or 0,
        total_carbs=total_carbs or 0,
        total_fats=total_fats or 0,
    )
