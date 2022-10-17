from authapp.forms import BlogUserLoginForm, BlogUserRegisterForm, BlogUserEditForm
from authapp.models import BlogUser
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


def login(request):
    login_form = BlogUserLoginForm(data=request.POST)

    next = request.GET.get('next', '')

    if request.method == 'POST' and login_form.is_valid:
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    content = {
        'title': 'Вход',
        'login_form': login_form,
        'next': next
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    if request.method == 'POST':
        register_form = BlogUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = BlogUserRegisterForm

    content = {
        'title': 'Регистрация',
        'form': register_form
    }
    return render(request, 'authapp/register.html', content)


def edit(request):
    if request.method == 'POST':
        edit_form = BlogUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = BlogUserEditForm(instance=request.user)
        user = BlogUser.objects.get(pk=request.user.pk)

    content = {
        'title': 'Редактирование',
        'edit_form': edit_form,
        'user': user

    }
    return render(request, 'authapp/edit.html', content)
