# Generated by Django 2.2 on 2020-02-23 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20200223_1703'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bibtex',
            name='note',
        ),
        migrations.AddField(
            model_name='bibtex',
            name='fund',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]