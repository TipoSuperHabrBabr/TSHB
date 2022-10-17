from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from authapp.forms import BlogUserLoginForm, BlogUserRegisterForm, BlogUserEditForm
from authapp.models import BlogUser


def password_change(request,
                    template_name='authapp/change_password.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    if post_change_redirect is None:
        post_change_redirect = reverse('auth:change_password_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Updating the password logs out all other sessions for the user
            # except the current one if
            # django.contrib.auth.middleware.SessionAuthenticationMiddleware
            # is enabled.
            update_session_auth_hash(request, form.user)
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
        'title': 'Password change',
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def password_change_done(request,
                         template_name='authapp/change_password_done.html',
                         current_app=None, extra_context=None):
    context = {
        'title': 'Password change successful',
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


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
