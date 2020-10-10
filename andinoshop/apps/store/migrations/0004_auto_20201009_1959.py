# Generated by Django 3.0.8 on 2020-10-10 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_productreview'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='brand',
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ManyToManyField(to='store.Brand'),
        ),
    ]
