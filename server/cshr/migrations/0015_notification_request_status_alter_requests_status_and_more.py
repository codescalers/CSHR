# Generated by Django 4.2.13 on 2024-07-17 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0014_merge_20240709_1128"),
    ]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="request_status",
            field=models.CharField(
                choices=[
                    ("approved", "Approved"),
                    ("rejected", "Rejected"),
                    ("pending", "Pending"),
                    ("requested_to_cancel", "Requested To Cancel"),
                    ("cancel_approved", "Cancel Approved"),
                    ("cancel_rejected", "Cancel Rejected"),
                    ("canceled", "Canceled"),
                ],
                default="",
                max_length=20,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="requests",
            name="status",
            field=models.CharField(
                choices=[
                    ("approved", "Approved"),
                    ("rejected", "Rejected"),
                    ("pending", "Pending"),
                    ("requested_to_cancel", "Requested To Cancel"),
                    ("cancel_approved", "Cancel Approved"),
                    ("cancel_rejected", "Cancel Rejected"),
                    ("canceled", "Canceled"),
                ],
                max_length=20,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="notification",
            unique_together={("request_status", "request")},
        ),
    ]
