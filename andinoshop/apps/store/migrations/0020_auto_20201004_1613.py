# Generated by Django 3.0.8 on 2020-10-04 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_auto_20201004_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]