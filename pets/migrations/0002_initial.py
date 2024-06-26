# Generated by Django 5.0.1 on 2024-01-30 16:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("pets", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="pet",
            name="petowner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="pets",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="weightrecord",
            name="pet",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="weight_records",
                to="pets.pet",
            ),
        ),
    ]
