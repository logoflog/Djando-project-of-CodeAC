# Generated by Django 4.1.3 on 2023-01-16 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="books",
            name="bookImage",
            field=models.ImageField(default="1.png", upload_to="img"),
        ),
        migrations.AlterField(
            model_name="books",
            name="bookPress",
            field=models.CharField(default="出版社", max_length=20),
        ),
    ]
