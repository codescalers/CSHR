# Generated by Django 4.1 on 2022-09-04 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0016_event"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Company_properties",
            new_name="CompanyProperties",
        ),
        migrations.RenameModel(
            old_name="HR_LETTERS",
            new_name="HrLetters",
        ),
        migrations.AlterModelOptions(
            name="companyproperties",
            options={
                "verbose_name": "Company Property",
                "verbose_name_plural": "Company Properties",
            },
        ),
        migrations.AlterModelOptions(
            name="evaluations",
            options={
                "verbose_name": "Evaluation",
                "verbose_name_plural": "Evaluations",
            },
        ),
        migrations.AlterModelOptions(
            name="hrletters",
            options={"verbose_name": "Hr Letter", "verbose_name_plural": "Hr letters"},
        ),
        migrations.AlterModelOptions(
            name="requests",
            options={"verbose_name": "Request", "verbose_name_plural": "Requests"},
        ),
        migrations.AlterModelOptions(
            name="userskills",
            options={"verbose_name": "Skill", "verbose_name_plural": "Skills"},
        ),
        migrations.AlterModelOptions(
            name="trainingcourses",
            options={
                "verbose_name": "Training course",
                "verbose_name_plural": "Training courses",
            },
        ),
        migrations.AlterModelOptions(
            name="userevaluations",
            options={
                "verbose_name": "User Evaluation",
                "verbose_name_plural": "User Evaluations",
            },
        ),
    ]