# Generated by Django 2.2 on 2022-05-13 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.BinaryField(editable=True, max_length=68719476736),
        ),
        migrations.AlterField(
            model_name='file',
            name='filename',
            field=models.CharField(max_length=100),
        ),
    ]
