# Generated by Django 4.0.5 on 2022-10-13 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('batch', '0001_initial'),
        ('branch', '0001_initial'),
        ('student', '0002_student_fathers_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='batch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='batch.batch'),
        ),
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='branch.branch'),
        ),
    ]