# Generated by Django 5.1.3 on 2024-12-02 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0024_alter_wines_grapes_alter_wines_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spirits',
            name='Style',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
