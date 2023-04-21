# Generated by Django 4.1.5 on 2023-01-23 09:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="house_number",
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AlterField(
            model_name="indipred",
            name="indebtedness",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=25,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
        migrations.AlterField(
            model_name="retailsnet",
            name="indebtedness",
            field=models.DecimalField(
                decimal_places=2,
                default=0.0,
                max_digits=25,
                validators=[django.core.validators.MinValueValidator(0)],
            ),
        ),
    ]
