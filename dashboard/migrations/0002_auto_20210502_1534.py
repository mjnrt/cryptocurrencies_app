# Generated by Django 3.1.8 on 2021-05-02 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currentprices',
            name='average_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='currentprices',
            name='highest_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='currentprices',
            name='lowest_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
