# Generated by Django 4.0.5 on 2022-11-20 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('semester', '0004_merge_20221112_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='semester',
            name='credit',
        ),
    ]
