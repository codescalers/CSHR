# Generated by Django 4.1 on 2022-09-01 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0017_alter_user_options_rename_userskills_user_skills_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="social_insurance_number",
            field=models.CharField(default="123 456 789", max_length=45),
            preserve_default=False,
        ),
    ]
