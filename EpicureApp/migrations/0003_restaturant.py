# Generated by Django 4.2 on 2023-05-18 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EpicureApp', '0002_usersinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaturant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('RestaturantId', models.CharField(max_length=100)),
                ('RestaturantName', models.CharField(max_length=100)),
                ('RestaturantType', models.CharField(choices=[('Restaurant', 'Restaurant'), ('Fast Food', 'Fast Food'), ('Canteen', 'Canteen')], max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('address', models.CharField(default='null', max_length=100)),
                ('city', models.CharField(default='null', max_length=100)),
                ('state', models.CharField(default='null', max_length=100)),
                ('country', models.CharField(default='null', max_length=100)),
                ('pincode', models.CharField(default='null', max_length=100)),
                ('Documents', models.FileField(upload_to='documents/')),
            ],
        ),
    ]