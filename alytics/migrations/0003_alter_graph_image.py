# Generated by Django 3.2.4 on 2021-06-14 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alytics', '0002_auto_20210614_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graph',
            name='image',
            field=models.FilePathField(null=True, verbose_name='image'),
        ),
    ]
