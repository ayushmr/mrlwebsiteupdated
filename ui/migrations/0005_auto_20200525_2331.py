# Generated by Django 3.0.5 on 2020-05-25 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ui', '0004_maintable_limit_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='officialdefinitionsofproduct',
            old_name='pubishedcommodity',
            new_name='publishedcommodity',
        ),
    ]
