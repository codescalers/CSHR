# Generated by Django 4.2.9 on 2024-02-08 11:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0003_remove_vacationbalance_office_vacation_balance_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vacationbalance",
            name="actual_balance",
        ),
        migrations.AddField(
            model_name="vacationbalance",
            name="office_vacation_balance",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="cshr.officevacationbalance",
            ),
        ),
    ]
