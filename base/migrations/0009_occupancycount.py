# Generated by Django 4.1.7 on 2023-03-11 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_user_is_driver_user_license_no_user_vechile_no'),
    ]

    operations = [
        migrations.CreateModel(
            name='OccupancyCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_id', models.IntegerField()),
                ('total_count', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]