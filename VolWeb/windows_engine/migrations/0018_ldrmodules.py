# Generated by Django 3.2.15 on 2022-12-27 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investigations', '0001_initial'),
        ('windows_engine', '0017_sessions'),
    ]

    operations = [
        migrations.CreateModel(
            name='LdrModules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Base', models.BigIntegerField(null=True)),
                ('InInit', models.TextField(null=True)),
                ('InLoad', models.TextField(null=True)),
                ('InMem', models.TextField(null=True)),
                ('MappedPath', models.TextField(null=True)),
                ('Pid', models.IntegerField(null=True)),
                ('Process', models.CharField(choices=[('Evidence', 'Evidence'), ('Suspicious', 'Suspicious')], max_length=11, null=True)),
                ('investigation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='windows_ldrmodules_investigation', to='investigations.uploadinvestigation')),
            ],
        ),
    ]
