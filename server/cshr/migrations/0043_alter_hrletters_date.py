# Generated by Django 4.0.7 on 2022-09-18 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0042_alter_hrletters_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="hrletters",
            name="date",
            field=models.DateField(auto_now=True),
        ),
    ]
