# Generated by Django 4.2 on 2023-05-16 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EpicureApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsersInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(default='null', max_length=100)),
                ('RestaturantName', models.CharField(default='null', max_length=100)),
                ('RestaturantId', models.CharField(default='null', max_length=100)),
            ],
        ),
    ]