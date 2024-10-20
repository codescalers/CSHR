# Generated by Django 4.2.13 on 2024-07-04 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0011_notification_object_id_notification_object_type"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="notification",
            name="object_id",
        ),
        migrations.RemoveField(
            model_name="notification",
            name="object_type",
        ),
        migrations.AddField(
            model_name="notification",
            name="request",
            field=models.ForeignKey(
                default=102,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="notification_request",
                to="cshr.requests",
            ),
            preserve_default=False,
        ),
    ]
