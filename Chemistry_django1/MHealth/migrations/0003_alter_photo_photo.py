# Generated by Django 3.2.8 on 2021-10-22 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MHealth', '0002_alter_photo_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='photo',
            field=models.ImageField(upload_to='imgs'),
        ),
    ]
