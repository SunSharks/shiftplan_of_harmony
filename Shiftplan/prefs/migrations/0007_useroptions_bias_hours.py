# Generated by Django 3.2.18 on 2023-04-17 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prefs', '0006_useroptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='useroptions',
            name='bias_hours',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
