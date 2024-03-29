# Generated by Django 3.1 on 2020-11-03 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('language', models.CharField(choices=[('ben', 'Bangla'), ('eng', 'English'), ('ben+eng', 'Bangla & English')], default='ben', max_length=20)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='UploadImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images/')),
                ('text', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('language', models.CharField(choices=[('ben', 'Bangla'), ('eng', 'English'), ('ben+eng', 'Bangla & English')], default='ben', max_length=20)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
