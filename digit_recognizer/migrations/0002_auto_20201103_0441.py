# Generated by Django 3.1 on 2020-11-03 04:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('digit_recognizer', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UploadImage',
            new_name='StoreImageForHCR',
        ),
    ]
