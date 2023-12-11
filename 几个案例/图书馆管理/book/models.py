from django.db import models

# Create your models here.

class Books(models.Model):
    bookId = models.IntegerField(null=False, unique=True)
    bookName = models.CharField(max_length=30, default='Python')
    bookAuthor = models.CharField(max_length=20, default='佚名')
    bookPress = models.CharField(max_length=20, default='清华大学出版社')
    bookPrice = models.FloatField(default=20)
    bookImage = models.ImageField(upload_to='book', default='1.png')
