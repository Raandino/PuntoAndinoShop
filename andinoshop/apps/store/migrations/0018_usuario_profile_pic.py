# Generated by Django 3.0.8 on 2020-10-04 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_usuario_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
