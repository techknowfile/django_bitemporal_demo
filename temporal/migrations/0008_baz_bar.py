# Generated by Django 3.0 on 2021-03-30 21:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('temporal', '0007_auto_20210330_2043'),
    ]

    operations = [
        migrations.AddField(
            model_name='baz',
            name='bar',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='baz', to='temporal.Bar'),
            preserve_default=False,
        ),
    ]
