# Generated by Django 4.0.7 on 2022-10-12 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cshr', '0052_remove_vacationbalance_emergency_leavess_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacation',
            name='reason',
            field=models.CharField(choices=[('public_holidays', 'Public Holidays'), ('emergency_leaves', 'Emergency Leave'), ('annual_leaves', 'Annual Leaves'), ('leave_excuses', 'Leave Excuses'), ('sick_leaves', 'Sick Leave'), ('unpaid', 'unpaid'), ('compensation', 'compensation')], default='annual_leaves', max_length=20),
        ),
    ]