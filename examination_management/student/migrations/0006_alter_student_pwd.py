# Generated by Django 4.0.5 on 2022-12-23 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_rename_soe_student_state_of_eligibility'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='pwd',
            field=models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No')], max_length=3, null=True, verbose_name='PwD'),
        ),
    ]
