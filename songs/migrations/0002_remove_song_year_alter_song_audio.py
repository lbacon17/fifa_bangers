# Generated by Django 4.0.3 on 2022-05-02 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('songs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='year',
        ),
        migrations.AlterField(
            model_name='song',
            name='audio',
            field=models.FileField(upload_to='audio'),
        ),
    ]
