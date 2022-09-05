# Generated by Django 4.1 on 2022-08-14 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0005_alter_user_mobilenumber_alter_user_telegramlink"),
    ]

    operations = [
        migrations.RenameField(
            model_name="company_properties",
            old_name="user_id",
            new_name="user",
        ),
        migrations.RenameField(
            model_name="userskills",
            old_name="Name",
            new_name="name",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="Birthday",
            new_name="birthday",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="Email",
            new_name="email",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="FirstName",
            new_name="first_name",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="LastName",
            new_name="last_name",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="Location_id",
            new_name="location",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="MobileNumber",
            new_name="mobile_number",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="UserSkills_ids",
            new_name="userskills",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="Team",
            new_name="team",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="TelegramLink",
            new_name="telegram_link",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="User_type",
            new_name="user_type",
        ),
        migrations.RemoveField(
            model_name="user",
            name="Salary",
        ),
        migrations.AddField(
            model_name="user",
            name="salary",
            field=models.JSONField(default=dict),
        ),
    ]
