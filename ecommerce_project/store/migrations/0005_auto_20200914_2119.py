# Generated by Django 3.1.1 on 2020-09-14 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20200902_1832'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingaddress',
            old_name='adress',
            new_name='address',
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='country',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
