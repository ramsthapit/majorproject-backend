# Generated by Django 4.1.3 on 2022-12-22 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0002_remove_geolocation_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="geolocation",
            name="lat",
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name="geolocation",
            name="lon",
            field=models.FloatField(null=True),
        ),
    ]
