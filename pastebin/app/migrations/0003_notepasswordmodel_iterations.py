# Generated by Django 5.0.3 on 2024-03-23 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_notepasswordmodel_notemodel_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='notepasswordmodel',
            name='iterations',
            field=models.IntegerField(default=100000),
        ),
    ]
