# Generated by Django 4.1 on 2022-09-04 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0018_user_social_insurance_number"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Training_Courses",
            new_name="TrainingCourses",
        ),
    ]