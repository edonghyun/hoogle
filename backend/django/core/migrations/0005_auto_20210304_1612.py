# Generated by Django 3.1.7 on 2021-03-04 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_doc2vecmodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='doc2vecmodel',
            old_name='instance',
            new_name='_instance',
        ),
    ]
