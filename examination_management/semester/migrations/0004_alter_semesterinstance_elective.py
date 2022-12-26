# Generated by Django 4.0.5 on 2022-12-23 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0001_initial'),
        ('semester', '0003_semesterinstance_sr_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semesterinstance',
            name='elective',
            field=models.ManyToManyField(blank=True, related_name='elective_semester_instance', to='subject.subject'),
        ),
    ]
