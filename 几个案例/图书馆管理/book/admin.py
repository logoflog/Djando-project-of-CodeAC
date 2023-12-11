from django.contrib import admin

# Register your models here.

from book import models

admin.site.register(models.Books)
