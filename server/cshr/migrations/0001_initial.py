# Generated by Django 4.1.2 on 2024-01-01 07:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import cshr.utils.generate


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("first_name", models.CharField(max_length=45)),
                ("last_name", models.CharField(max_length=45)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_image/"
                    ),
                ),
                (
                    "background_color",
                    models.CharField(
                        default=cshr.utils.generate.generate_random_color,
                        max_length=10,
                    ),
                ),
                ("email", models.EmailField(max_length=45, unique=True)),
                ("mobile_number", models.CharField(max_length=15)),
                ("telegram_link", models.CharField(max_length=100)),
                ("birthday", models.DateField()),
                ("joining_at", models.DateField()),
                (
                    "team",
                    models.CharField(
                        choices=[
                            ("Business Development", "Businessdevelopment"),
                            ("Development", "Development"),
                            ("HR & Finance", "Hrandfinance"),
                            ("QA", "Qa"),
                            ("Marketing", "Marketing"),
                            ("Operations", "Operations"),
                            ("Support", "Support"),
                        ],
                        max_length=20,
                    ),
                ),
                ("salary", models.JSONField(blank=True, default=dict, null=True)),
                (
                    "user_type",
                    models.CharField(
                        choices=[
                            ("Admin", "admin"),
                            ("User", "user"),
                            ("Supervisor", "supervisor"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        choices=[("Male", "male"), ("Female", "female")], max_length=20
                    ),
                ),
                ("social_insurance_number", models.CharField(max_length=45)),
                ("address", models.CharField(max_length=150)),
                ("job_title", models.CharField(max_length=150)),
                ("is_admin", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Evaluations",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "form",
                    models.CharField(
                        choices=[
                            ("Peer 2 Peer Form", "Peer 2 Peer Form"),
                            ("Reverse Form", "Reverse Form"),
                        ],
                        max_length=50,
                    ),
                ),
                (
                    "quarter",
                    models.CharField(
                        choices=[
                            ("1 : 3", "Jan March"),
                            ("4 : 6", "Apr Jun"),
                            ("7 : 9", "Jul Sep"),
                            ("10 : 12", "Oct Dec"),
                        ],
                        max_length=150,
                    ),
                ),
                ("link", models.CharField(max_length=150)),
            ],
            options={
                "verbose_name": "Evaluation",
                "verbose_name_plural": "Evaluations",
            },
        ),
        migrations.CreateModel(
            name="Office",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=45, unique=True)),
                ("country", models.CharField(max_length=45)),
                (
                    "weekend",
                    models.CharField(
                        choices=[
                            ("Friday:Saturday", "Friday:Saturday"),
                            ("Saturday:Sunday", "Saturday:Sunday"),
                        ],
                        default="Friday:Saturday",
                        max_length=20,
                    ),
                ),
            ],
            options={
                "unique_together": {("name", "country")},
            },
        ),
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("hr_letters", "HR Letters"),
                            ("compensations", "Compensations"),
                            ("vacations", "Vacations"),
                            ("official-document", "Official document"),
                        ],
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
                        max_length=20,
                    ),
                ),
                (
                    "applying_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="apply_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "approval_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="approve_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Request",
                "verbose_name_plural": "Requests",
            },
        ),
        migrations.CreateModel(
            name="UserSkills",
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
                ("name", models.CharField(max_length=50)),
            ],
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
            options={
                "abstract": False,
            },
            bases=("cshr.requests",),
        ),
        migrations.CreateModel(
            name="HrLetters",
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
                ("with_salary_mentioned", models.BooleanField(default=False)),
                ("with_date", models.BooleanField(default=False)),
                ("from_date", models.DateField(blank=True, null=True)),
                ("end_date", models.DateField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Hr Letter",
                "verbose_name_plural": "Hr letters",
            },
            bases=("cshr.requests",),
        ),
        migrations.CreateModel(
            name="OffcialDocument",
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
                ("document", models.TextField()),
            ],
            options={
                "abstract": False,
            },
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
                            ("public_holidays", "Public Holidays"),
                            ("emergency_leaves", "Emergency Leave"),
                            ("annual_leaves", "Annual Leaves"),
                            ("leave_excuses", "Leave Excuses"),
                            ("sick_leaves", "Sick Leave"),
                            ("unpaid", "unpaid"),
                            ("compensation", "compensation"),
                        ],
                        default="annual_leaves",
                        max_length=20,
                    ),
                ),
                ("from_date", models.DateField()),
                ("end_date", models.DateField()),
                ("change_log", models.JSONField(default=list)),
                ("actual_days", models.IntegerField(default=0)),
            ],
            options={
                "abstract": False,
            },
            bases=("cshr.requests",),
        ),
        migrations.CreateModel(
            name="VacationBalance",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("sick_leaves", models.IntegerField()),
                ("compensation", models.IntegerField()),
                ("unpaid", models.IntegerField()),
                ("annual_leaves", models.IntegerField()),
                ("emergency_leaves", models.IntegerField()),
                ("leave_excuses", models.IntegerField()),
                ("actual_balance", models.JSONField(default=dict, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="UserEvaluations",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                (
                    "quarter",
                    models.CharField(
                        choices=[
                            ("1 : 3", "Jan March"),
                            ("4 : 6", "Apr Jun"),
                            ("7 : 9", "Jul Sep"),
                            ("10 : 12", "Oct Dec"),
                        ],
                        max_length=150,
                    ),
                ),
                ("link", models.CharField(max_length=150)),
                ("score", models.IntegerField(default=0)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "User Evaluation",
                "verbose_name_plural": "User Evaluations",
            },
        ),
        migrations.CreateModel(
            name="UserDocuments",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("image", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("approved", "Approved"),
                            ("Under-review", "under-review"),
                            ("Rejected", "rejected"),
                        ],
                        default="Under-review",
                        max_length=20,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="TrainingCourses",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=45)),
                ("certificate_link", models.CharField(max_length=150)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_courses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Training course",
                "verbose_name_plural": "Training courses",
            },
        ),
        migrations.CreateModel(
            name="PublicHoliday",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("holiday_date", models.DateField()),
                ("expired", models.BooleanField(default=False)),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cshr.office"
                    ),
                ),
            ],
            options={
                "unique_together": {("holiday_date", "location")},
            },
        ),
        migrations.CreateModel(
            name="Meetings",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("location", models.CharField(default="remote", max_length=250)),
                ("meeting_link", models.CharField(max_length=250)),
                ("date", models.DateTimeField()),
                (
                    "host_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="host_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "invited_users",
                    models.ManyToManyField(
                        related_name="invited_users", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "Meeting",
                "verbose_name_plural": "Meetings",
            },
        ),
        migrations.CreateModel(
            name="Event",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=40)),
                ("description", models.CharField(max_length=200)),
                ("location", models.TextField(max_length=300, null=True)),
                ("from_date", models.DateTimeField(null=True)),
                ("end_date", models.DateTimeField(null=True)),
                (
                    "people",
                    models.ManyToManyField(
                        related_name="event_participants", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
            options={
                "verbose_name": "Event",
                "verbose_name_plural": "Events",
            },
        ),
        migrations.CreateModel(
            name="CompanyProperties",
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
                ("name", models.CharField(max_length=45)),
                ("image_of", models.ImageField(blank=True, null=True, upload_to="")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Company Property",
                "verbose_name_plural": "Company Properties",
            },
        ),
        migrations.AddField(
            model_name="user",
            name="location",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="cshr.office"
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="reporting_to",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="user",
            name="skills",
            field=models.ManyToManyField(
                blank=True, related_name="skills", to="cshr.userskills"
            ),
        ),
        migrations.CreateModel(
            name="OfficeVacationBalance",
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
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("modified_at", models.DateTimeField(auto_now=True)),
                ("year", models.IntegerField(default=2024)),
                ("annual_leaves", models.IntegerField(default=20)),
                ("sick_leaves", models.IntegerField(default=365)),
                ("compensation", models.IntegerField(default=365)),
                ("unpaid", models.IntegerField(default=365)),
                ("leave_excuses", models.IntegerField(default=6)),
                ("emergency_leaves", models.IntegerField(default=6)),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="cshr.office"
                    ),
                ),
                (
                    "public_holidays",
                    models.ManyToManyField(
                        related_name="public_holidays", to="cshr.publicholiday"
                    ),
                ),
            ],
            options={
                "unique_together": {("year", "location")},
            },
        ),
    ]
