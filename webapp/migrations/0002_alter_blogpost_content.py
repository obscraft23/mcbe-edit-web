# Generated by Django 4.1.7 on 2023-03-04 01:32

from django.db import migrations
import jsoneditor.fields.django3_jsonfield


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=jsoneditor.fields.django3_jsonfield.JSONField(),
        ),
    ]
