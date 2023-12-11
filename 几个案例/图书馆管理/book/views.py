from . import models, forms
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.

def hello(request):
    # if request.user.is_authenticated:
    print(request.GET)
    return render(request, 'hello.html', None)

@login_required(login_url='/login/')
def index(request, pid=None, del_pass=None):
    # if request.user.is_authenticated:
    username = request.user.username
    email = request.user.email
    x = 'img/1.png'
    return render(request, 'index.html', locals())

def login(request):
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            login_name = request.POST['username'].strip()
            login_password = request.POST['password']
            user = authenticate(username=login_name, password=login_password)
            if user is not None:
                if user.is_active:
                    auth.login(request, user)
                    print("success")
                    messages.add_message(request, messages.SUCCESS, 
                                         user.username + '已登录')
                    return redirect('/')
                else:
                    messages.add_message(request, messages.WARNING, 
                                         '账号未激活')
            else:
                messages.add_message(request, messages.WARNING, 
                                     '登录失败')
        else:
            messages.add_message(request, messages.INFO,
                                 '请检查输入的內容')
    else:
        login_form = forms.LoginForm()
    return render(request, 'login.html', locals())

@login_required(login_url='/login/')
def logout(request):
    username = request.user.username
    auth.logout(request)
    messages.add_message(request, messages.INFO, username+"已注销")
    return redirect('/')

@login_required(login_url='/login/')
def add(request):
    username = request.user.username
    if request.method == 'GET':
        book_form = forms.BookForm()
    else:
        book_form = forms.BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            book_form.save()  
            messages.add_message(request, messages.SUCCESS, '已保存')
            return redirect('/add')
        else:
            messages.add_message(request, messages.INFO, '请填写所有字段')
    return render(request, 'add.html', locals())    

@login_required(login_url='/login/')
def select(request):
    username = request.user.username
    if request.method == 'GET':
        book_values = None
    else:
        book_name = request.POST['book_name']
        # print('-'*10, book_name)
        book_values = models.Books.objects.filter(bookName__contains=book_name).order_by('bookId')
    return render(request, 'select.html', locals())    

@login_required(login_url='/login/')
def update(request):
    username = request.user.username
    if request.method == 'GET':
        book_values = None
    else:
        book_name = request.POST['book_name']
        book_values = models.Books.objects.filter(bookName__contains=book_name).order_by('bookId')
    return render(request, 'update.html', locals())    

@login_required(login_url='/login/')
def update_confirm(request):
    if request.method == 'GET':
        username = request.user.username
        book_id = request.GET['book_id']
        book_obj = models.Books.objects.get(bookId=book_id)
        book_form = forms.BookForm(instance=book_obj)
        return render(request, 'update_confirm.html', locals())    
    else:
        book_id = request.POST['bookId']
        book = models.Books.objects.get(bookId=book_id)
        book_form = forms.BookForm(data=request.POST, 
                                   files=request.FILES, 
                                   instance=book)
        book_form.save()
        messages.add_message(request, messages.SUCCESS, '已保存')
        return redirect('/update')
    return render(request, 'update.html', locals())    


@login_required(login_url='/login/')
def delete(request, book_id=None):
    username = request.user.username
    if request.method == 'GET':
        if book_id:
            book_value = models.Books.objects.filter(bookId=book_id)
            if len(book_value) == 0:
                book_value = None
            else:
                book_value[0].delete()
        book_value = None
        return render(request, 'delete.html', locals())    
    else:
        book_name = request.POST['book_name']
        book_values = models.Books.objects.filter(bookName__contains=book_name).order_by('bookId')
        print(book_values)
        return render(request, 'delete.html', locals())    

