# Generated by Django 3.0.8 on 2020-10-01 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_product_subcategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('ordering',), 'verbose_name_plural': 'Categories'},
        ),
        migrations.AddField(
            model_name='category',
            name='ordering',
            field=models.IntegerField(default=0),
        ),
    ]