# Generated by Django 4.1.2 on 2023-12-15 09:52

from datetime import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0085_vacation_actual_days"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="joining_at",
            field=models.DateField(default=datetime.now().date()),
            preserve_default=False,
        ),
    ]
