# Generated by Django 5.1.3 on 2024-11-22 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0015_alter_spirits_style'),
    ]

    operations = [
        migrations.AddField(
            model_name='wines',
            name='type',
            field=models.CharField(default=2, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='wines',
            name='grapes',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='wines',
            name='region',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AlterField(
            model_name='wines',
            name='year',
            field=models.IntegerField(default=' '),
        ),
    ]
