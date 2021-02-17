# Generated by Django 3.0 on 2021-02-17 03:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('temporal', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fooversion',
            options={'ordering': ('valid_start_date',)},
        ),
        migrations.AddField(
            model_name='fooversion',
            name='sys_end_date',
            field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999)),
        ),
        migrations.AddField(
            model_name='fooversion',
            name='sys_start_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='fooversion',
            name='valid_end_date',
            field=models.DateField(default='9999-12-31'),
            preserve_default=False,
        ),
    ]
