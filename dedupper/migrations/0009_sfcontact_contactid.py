# Generated by Django 2.0.5 on 2018-06-17 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dedupper', '0008_auto_20180615_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='sfcontact',
            name='ContactID',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]
