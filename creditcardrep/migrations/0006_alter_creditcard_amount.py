# Generated by Django 4.0.6 on 2022-08-04 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditcardrep', '0005_alter_creditcard_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditcard',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
