# Generated by Django 3.2.4 on 2021-06-14 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alytics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graph',
            name='points',
        ),
        migrations.AddField(
            model_name='graph',
            name='error',
            field=models.CharField(max_length=511, null=True, verbose_name='error'),
        ),
        migrations.AddField(
            model_name='graph',
            name='image',
            field=models.FileField(null=True, upload_to='plot/', verbose_name='image'),
        ),
    ]
