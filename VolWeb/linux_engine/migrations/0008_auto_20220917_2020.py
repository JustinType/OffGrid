# Generated by Django 3.2.13 on 2022-09-17 20:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('linux_engine', '0007_elfs'),
    ]

    operations = [
        migrations.AddField(
            model_name='bash',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='elfs',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='lsof',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='procmaps',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='ttycheck',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
    ]
