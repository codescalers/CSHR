# Generated by Django 4.1.2 on 2023-11-05 07:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0072_rename_date_publicholiday_holiday_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="location",
            field=models.TextField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name="event",
            name="people",
            field=models.ManyToManyField(
                null=True,
                related_name="event_participants",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]