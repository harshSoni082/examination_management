# Generated by Django 4.0.5 on 2022-11-18 13:09

import django.core.validators
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is_deleted')),
                ('code', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Code')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
                ('credit', models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Credit')),
                ('is_elective', models.BooleanField(default=False, verbose_name='Is Elective')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
