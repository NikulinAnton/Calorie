from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import RegexValidator
from django.db import models
from django_paranoid.models import ParanoidModel

from core.fields import CIEmailField
from core.managers import CUserManager

phone_validate = RegexValidator(r"\d+", "Phone should be numerical")


class CUser(AbstractBaseUser, ParanoidModel):
    mobile = models.CharField(
        max_length=21,
        verbose_name="Mobile number",
        help_text="Format 71111111111",
        null=True,
        blank=True,
        validators=[phone_validate],
    )
    email = CIEmailField(verbose_name="Email", unique=True, max_length=512)
    first_name = models.CharField(max_length=150, null=True)
    last_name = models.CharField(max_length=150, null=True)
    is_superuser = models.BooleanField(verbose_name="Superuser status", default=False)
    fav_foods = models.ManyToManyField("Food")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CUserManager()

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name or ''}"

    def __str__(self):
        return f"{self.pk} {self.get_username()}"


class Diet(ParanoidModel):
    foods = models.ManyToManyField("Food", through="DietFood")
    owner = models.ForeignKey(CUser, on_delete=models.PROTECT)
    date = models.DateField(db_index=True)

    @property
    def diet_foods(self):
        return DietFood.objects.filter(diet=self.id)

    class Meta:
        unique_together = ["owner", "date"]
        ordering = ["date"]

    def __str__(self):
        return f"{self.pk}: {self.owner} {self.date}"


class DietFood(models.Model):
    diet = models.ForeignKey(Diet, on_delete=models.PROTECT, related_name="diet_foods")
    food = models.ForeignKey("Food", on_delete=models.PROTECT, null=True)
    quantity = models.PositiveIntegerField()

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.pk}: {self.food}"


class Food(ParanoidModel):
    owner = models.ForeignKey(CUser, on_delete=models.PROTECT, null=True)
    name = models.CharField(max_length=255, db_index=True)
    calories = models.FloatField()
    proteins = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()

    class Meta:
        unique_together = ["owner", "name"]
        ordering = ["name"]

    def __str__(self):
        return f"{self.pk}: {self.name}"
