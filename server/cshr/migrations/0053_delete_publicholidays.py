# Generated by Django 4.0.7 on 2022-10-18 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0052_rename_userdocements_userdocuments"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PublicHolidays",
        ),
    ]