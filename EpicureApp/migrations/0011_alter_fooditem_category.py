# Generated by Django 4.2 on 2023-05-20 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EpicureApp', '0010_alter_fooditem_restaturantid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fooditem',
            name='Category',
            field=models.CharField(choices=[('Snacks', 'Snacks'), ('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')], max_length=100),
        ),
    ]
