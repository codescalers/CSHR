# Generated by Django 4.2.9 on 2024-03-12 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0004_remove_vacationbalance_actual_balance_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="social_insurance_number",
            field=models.CharField(blank=True, max_length=45, null=True),
        ),
    ]