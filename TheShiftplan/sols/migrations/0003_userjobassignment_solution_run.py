# Generated by Django 3.2.18 on 2023-05-26 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sols', '0002_solutionrun'),
    ]

    operations = [
        migrations.AddField(
            model_name='userjobassignment',
            name='solution_run',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='sols.solutionrun'),
            preserve_default=False,
        ),
    ]
