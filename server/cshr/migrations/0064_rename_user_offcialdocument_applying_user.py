# Generated by Django 4.1.2 on 2022-10-23 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0063_offcialdocument_type_alter_requests_type"),
    ]

    operations = [
        migrations.RenameField(
            model_name="offcialdocument",
            old_name="user",
            new_name="applying_user",
        ),
    ]
