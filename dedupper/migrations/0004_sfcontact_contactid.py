# Generated by Django 2.0.5 on 2018-06-21 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dedupper', '0003_auto_20180621_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='sfcontact',
            name='ContactID',
            field=models.CharField(blank=True, max_length=128),
        ),
    ]