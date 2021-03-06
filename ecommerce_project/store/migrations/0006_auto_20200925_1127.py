# Generated by Django 3.1.1 on 2020-09-25 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20200914_2119'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='device',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='digital',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='../static/images/default.png', upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
