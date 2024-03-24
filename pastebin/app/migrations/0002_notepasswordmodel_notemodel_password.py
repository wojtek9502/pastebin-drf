# Generated by Django 5.0.3 on 2024-03-23 15:48

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotePasswordModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('inserted_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('password_hash', models.BinaryField()),
                ('salt', models.BinaryField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='notemodel',
            name='password',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.notepasswordmodel'),
        ),
    ]
