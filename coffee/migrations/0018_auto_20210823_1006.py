# Generated by Django 3.2 on 2021-08-23 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0017_auto_20210822_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='countries',
            name='region',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='countries',
            name='subregion',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
