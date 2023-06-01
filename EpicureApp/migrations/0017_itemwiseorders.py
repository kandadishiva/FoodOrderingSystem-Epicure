# Generated by Django 4.2 on 2023-05-26 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EpicureApp', '0016_restaturant_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemWiseOrders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OrderId', models.CharField(max_length=100)),
                ('ItemId', models.CharField(max_length=100)),
                ('ItemName', models.CharField(max_length=100)),
                ('Quantity', models.CharField(max_length=100)),
                ('Price', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
            ],
        ),
    ]
