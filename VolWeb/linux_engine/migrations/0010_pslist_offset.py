# Generated by Django 3.2.15 on 2022-12-27 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linux_engine', '0009_pslist_tid'),
    ]

    operations = [
        migrations.AddField(
            model_name='pslist',
            name='Offset',
            field=models.BigIntegerField(null=True),
        ),
    ]
