# Generated by Django 5.1.3 on 2024-11-21 22:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_rename_id_wines_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('quantity', models.IntegerField()),
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('wine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_app.wines')),
            ],
        ),
    ]
