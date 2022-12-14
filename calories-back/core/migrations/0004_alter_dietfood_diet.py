# Generated by Django 4.1.1 on 2022-10-03 23:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0003_alter_diet_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dietfood",
            name="diet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="diet_foods",
                to="core.diet",
            ),
        ),
    ]
