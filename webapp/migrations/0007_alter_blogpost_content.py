# Generated by Django 3.2.18 on 2023-03-04 03:49

from django.db import migrations
import webapp.jsonwidget


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20230304_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=webapp.jsonwidget.JSONField(),
        ),
    ]
