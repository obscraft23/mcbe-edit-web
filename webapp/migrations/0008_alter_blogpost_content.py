# Generated by Django 3.2.18 on 2023-03-04 03:55

from django.db import migrations
import jsoneditor.fields.django3_jsonfield


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_alter_blogpost_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='content',
            field=jsoneditor.fields.django3_jsonfield.JSONField(),
        ),
    ]
