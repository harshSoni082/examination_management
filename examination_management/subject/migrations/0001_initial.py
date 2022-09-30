# Generated by Django 4.0.5 on 2022-09-30 12:18

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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='is_deleted')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Name')),
                ('credit', models.IntegerField(blank=True, null=True, verbose_name='Credit')),
                ('code', models.CharField(blank=True, db_index=True, max_length=100, null=True, unique=True, verbose_name='Code')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
