# Generated by Django 3.2 on 2021-09-04 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffee', '0025_recommendations_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendations',
            name='recs_set',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
