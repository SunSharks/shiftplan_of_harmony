# Generated by Django 4.1.3 on 2022-11-07 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('defs', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='day',
        ),
        migrations.RemoveField(
            model_name='jobtype',
            name='subgroup',
        ),
        migrations.RemoveField(
            model_name='shiftplan',
            name='group',
        ),
        migrations.AddField(
            model_name='jobtype',
            name='description',
            field=models.TextField(default='', verbose_name='description'),
        ),
        migrations.AddField(
            model_name='shiftplan',
            name='name',
            field=models.CharField(default='', max_length=200, unique=True, verbose_name='shiftplan name'),
        ),
        migrations.DeleteModel(
            name='Day',
        ),
        migrations.DeleteModel(
            name='Subgroup',
        ),
    ]
