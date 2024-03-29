# Generated by Django 3.2.13 on 2022-08-12 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('windows_engine', '0013_privs_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='cmdline',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='dlllist',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='envars',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='handles',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='hashdump',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='netscan',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='netstat',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='skeletonkeycheck',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='timeliner',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='userassist',
            name='Tag',
            field=models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True),
        ),
    ]
