# Generated by Django 3.1.2 on 2020-11-04 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_product_digital'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='colour',
            field=models.CharField(max_length=200),
        ),
    ]
