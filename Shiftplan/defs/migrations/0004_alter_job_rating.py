# Generated by Django 3.2.18 on 2023-03-29 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('defs', '0003_auto_20230329_2053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='rating',
            field=models.IntegerField(null=True, verbose_name='rating'),
        ),
    ]