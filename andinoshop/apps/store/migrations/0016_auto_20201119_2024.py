# Generated by Django 3.1.2 on 2020-11-20 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_auto_20201119_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
