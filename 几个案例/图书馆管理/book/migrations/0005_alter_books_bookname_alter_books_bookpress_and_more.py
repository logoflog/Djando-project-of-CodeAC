# Generated by Django 4.1.3 on 2023-01-19 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0004_alter_books_bookimage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="books",
            name="bookName",
            field=models.CharField(default="Python", max_length=30),
        ),
        migrations.AlterField(
            model_name="books",
            name="bookPress",
            field=models.CharField(default="清华大学出版社", max_length=20),
        ),
        migrations.AlterField(
            model_name="books",
            name="bookPrice",
            field=models.FloatField(default=20),
        ),
    ]
