import collections

from django_tiny_util.models import update_fields

from core.models import CUser, DietFood, Food


def create_dietfood(validated_data: dict, owner: CUser) -> DietFood:
    food_data = validated_data.pop("food")
    food = _update_or_create_food(food_data, owner)
    return DietFood.objects.create(**validated_data, food=food)


def update_dietfood(
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
