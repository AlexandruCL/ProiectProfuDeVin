# Generated by Django 5.1.3 on 2024-11-21 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wines',
            name='ID',
            field=models.AutoField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
