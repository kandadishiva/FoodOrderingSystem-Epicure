# Generated by Django 4.2 on 2023-05-19 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('EpicureApp', '0007_alter_fooditems_restaturantid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FoodItems',
        ),
    ]
