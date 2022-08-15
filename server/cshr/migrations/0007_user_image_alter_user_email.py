# Generated by Django 4.1 on 2022-08-15 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cshr", "0006_rename_user_id_company_properties_user_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="image",
            field=models.ImageField( upload_to=""),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=45, unique=True),
        ),
    ]
