# Generated by Django 4.2.9 on 2024-04-01 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0007_alter_vacation_end_date_alter_vacation_from_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vacation",
            name="actual_days",
            field=models.FloatField(default=0),
        ),
    ]
