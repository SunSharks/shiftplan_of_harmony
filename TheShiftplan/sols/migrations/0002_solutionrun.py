# Generated by Django 3.2.18 on 2023-05-26 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sols', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolutionRun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(verbose_name='solution run timestamp')),
                ('final', models.BooleanField(default=False)),
            ],
        ),
    ]