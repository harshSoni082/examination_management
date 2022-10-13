# Generated by Django 4.0.5 on 2022-10-12 12:42

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('batch', '0001_initial'),
        ('branch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is_deleted')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='Email')),
                ('roll_no', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Roll Number')),
                ('batch', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='batch.batch')),
                ('branch', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='branch.branch')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
