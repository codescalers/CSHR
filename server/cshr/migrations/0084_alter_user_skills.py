# Generated by Django 4.1.2 on 2023-11-28 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0083_remove_vacation_taked_from_old_balance_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="skills",
            field=models.ManyToManyField(
                blank=True, related_name="skills", to="cshr.userskills"
            ),
        ),
    ]
