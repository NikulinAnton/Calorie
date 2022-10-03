# Generated by Django 4.1.1 on 2022-10-03 22:37

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import core.fields
import core.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "deleted_at",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                (
                    "mobile",
                    models.CharField(
                        blank=True,
                        help_text="Format 71111111111",
                        max_length=21,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "\\d+", "Phone should be numerical"
                            )
                        ],
                        verbose_name="Mobile number",
                    ),
                ),
                (
                    "email",
                    core.fields.CIEmailField(
                        max_length=512, unique=True, verbose_name="Email"
                    ),
                ),
                ("first_name", models.CharField(max_length=150, null=True)),
                ("last_name", models.CharField(max_length=150, null=True)),
                (
                    "is_superuser",
                    models.BooleanField(default=False, verbose_name="Superuser status"),
                ),
            ],
            options={
                "abstract": False,
            },
            managers=[
                ("objects", core.managers.CUserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Diet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "deleted_at",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("date", models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name="Food",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "deleted_at",
                    models.DateTimeField(blank=True, default=None, null=True),
                ),
                ("name", models.CharField(db_index=True, max_length=255)),
                ("calories", models.FloatField()),
                ("proteins", models.FloatField()),
                ("carbs", models.FloatField()),
                ("fats", models.FloatField()),
                (
                    "owner",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("owner", "name")},
            },
        ),
        migrations.CreateModel(
            name="DietFood",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField()),
                (
                    "diet",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.diet"
                    ),
                ),
                (
                    "food",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="core.food",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="diet",
            name="foods",
            field=models.ManyToManyField(through="core.DietFood", to="core.food"),
        ),
        migrations.AddField(
            model_name="diet",
            name="owner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="cuser",
            name="fav_foods",
            field=models.ManyToManyField(to="core.food"),
        ),
        migrations.AlterUniqueTogether(
            name="diet",
            unique_together={("owner", "date")},
        ),
    ]
