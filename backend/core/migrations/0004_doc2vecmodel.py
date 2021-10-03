# Generated by Django 3.1.7 on 2021-03-03 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210303_1928'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doc2VecModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('epochs', models.IntegerField(default=0)),
                ('instance', models.BinaryField()),
            ],
            options={
                'db_table': 'doc2vec_models',
            },
        ),
    ]