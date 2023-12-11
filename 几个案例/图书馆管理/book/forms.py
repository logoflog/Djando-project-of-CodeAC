# -*- coding: utf-8 -*-

from django import forms
from . import models

class LoginForm(forms.Form):
    username = forms.CharField(label='姓名', max_length=10)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())

class BookForm(forms.ModelForm):
    class Meta:
        model = models.Books
        fields = '__all__'
        labels = {'bookId':'编 号',
                  'bookName':'名 称',
                  'bookPress':'出版社',
                  'bookAuthor':'作 者',
                  'bookPrice':'价 格',
                  'bookImage':'图 片'}
        
# 
