# Generated by Django 3.1.2 on 2020-10-15 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20201015_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='original_price',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
