# Generated by Django 5.0.1 on 2024-01-23 16:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("pets", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PetService",
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
                ("name", models.CharField(blank=True, max_length=100)),
                ("description", models.TextField()),
                (
                    "cost",
                    models.DecimalField(
                        decimal_places=2, help_text="Cost in dollars", max_digits=10
                    ),
                ),
                ("duration", models.IntegerField(help_text="Duration in days")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="PetServiceCategory",
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
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("DIAG", "Diagnostic"),
                            ("IMG", "Imaging"),
                            ("VET", "Veterinary Appointment"),
                            ("GRO", "Grooming"),
                        ],
                        max_length=4,
                        unique=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PetServiceTracker",
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
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("REQUESTED", "Requested"),
                            ("CONFIRMED_PAID", "Confirmed Paid"),
                            ("IN_PROGRESS", "In Progress"),
                            ("COMPLETED", "Completed"),
                            ("CANCELLED", "Cancelled"),
                        ],
                        default="REQUESTED",
                        max_length=50,
                    ),
                ),
                ("is_tracked", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True, max_length=50, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="PetRequestService",
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
                (
                    "paid",
                    models.BooleanField(default=False, verbose_name="Paid Status"),
                ),
                (
                    "stripe_session_id",
                    models.CharField(
                        blank=True,
                        max_length=500,
                        null=True,
                        verbose_name="Stripe Session ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "pet",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="requests_services",
                        to="pets.pet",
                    ),
                ),
            ],
        ),
    ]
