# Generated by Django 4.0.6 on 2022-08-01 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creditcardrep', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditcard',
            name='date',
            field=models.DateTimeField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='creditcard',
            name='prop_id',
            field=models.CharField(max_length=5),
            preserve_default=False,
        ),
    ]
