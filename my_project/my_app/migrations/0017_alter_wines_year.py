# Generated by Django 5.1.3 on 2024-11-22 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0016_rename_country_wines_country_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wines',
            name='Year',
            field=models.IntegerField(null=True),
        ),
    ]
