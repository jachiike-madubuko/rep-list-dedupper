# Generated by Django 2.0.5 on 2018-07-03 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dedupper', '0005_auto_20180703_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='deduptime',
            name='current_key',
            field=models.CharField(blank=True, max_length=256),
        ),
    ]
