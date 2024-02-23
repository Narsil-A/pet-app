# Generated by Django 5.0.1 on 2024-01-30 16:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("medicalvisit", "0002_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="petmedicalvisit",
            name="vet_staff",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="recorded_visits",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
