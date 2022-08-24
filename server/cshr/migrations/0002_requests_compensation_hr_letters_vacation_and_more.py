# Generated by Django 4.1 on 2022-08-11 16:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Requests",
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
                ("modified_at", models.DateTimeField(db_index=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("hr_letters", "HR Letters"),
                            ("compensation", "Compensation"),
                            ("vacations", "Vacations"),
                        ],
                        default="vacations",
                        max_length=20,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("rejected", "Rejected"),
                            ("pending", "Pending"),
                            ("approved", "Approved"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                (
                    "applying_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="apply_user",
                        to="cshr.user",
                    ),
                ),
                (
                    "approval_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="approve_user",
                        to="cshr.user",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Compensation",
            fields=[
                (
                    "requests_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cshr.requests",
                    ),
                ),
                ("reason", models.CharField(blank=True, max_length=250)),
                ("from_date", models.DateField()),
                ("end_date", models.DateField()),
            ],
            options={"abstract": False,},
            bases=("cshr.requests",),
        ),
        migrations.CreateModel(
            name="HR_LETTERS",
            fields=[
                (
                    "requests_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cshr.requests",
                    ),
                ),
                ("addresses", models.CharField(max_length=45)),
            ],
            options={"abstract": False,},
            bases=("cshr.requests",),
        ),
        migrations.CreateModel(
            name="Vacation",
            fields=[
                (
                    "requests_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="cshr.requests",
                    ),
                ),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("annual_leaves", "Annual Leaves"),
                            ("public_holidays", "Public Holidays"),
                            ("emergency_leave", "Emergency Leave"),
                            ("leave_excuses", "Leave Excuses"),
                        ],
                        default="annual_leaves",
                        max_length=20,
                    ),
                ),
                ("from_date", models.DateField()),
                ("end_date", models.DateField()),
                ("change_log", models.JSONField(default=list)),
            ],
            options={"abstract": False,},
            bases=("cshr.requests",),
        ),
        migrations.CreateModel(
            name="Training_Courses",
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
                ("modified_at", models.DateTimeField(db_index=True)),
                ("name", models.CharField(max_length=45)),
                ("certificate_link", models.CharField(max_length=150)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_courses",
                        to="cshr.user",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]
