from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url, get_object_or_404
from django.template.response import TemplateResponse
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.generic import DetailView
import datetime

from authapp.forms import BlogUserLoginForm, BlogUserRegisterForm, BlogUserEditForm, BannedForm
from authapp.models import BlogUser
from blogapp.models import Notification
from blogapp.models import Post


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

    next = request.GET.get("returnUrl")

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
        'title': '????????',
        'login_form': login_form,
        'next': next,
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
        'title': '??????????????????????',
        'form': register_form,
        'path': next,
    }
    return render(request, 'authapp/register.html', content)


def edit(request):
    user = BlogUser.objects.get(pk=request.user.pk)
    if request.method == 'POST':
        edit_form = BlogUserEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:user_read', args=[user.pk]))
    else:
        edit_form = BlogUserEditForm(instance=request.user)

    content = {
        'title': '????????????????????????????',
        'edit_form': edit_form,
        'user': user

    }
    return render(request, 'authapp/edit.html', content)


class UserDetailView(DetailView):
    model = BlogUser
    template_name = 'authapp/user_read.html'

    def get_context_data(self, **kwargs):
        ctx = super(UserDetailView, self).get_context_data(**kwargs)
        ctx['notification'] = Notification.objects.all().order_by('created_date')
        user_pk = ctx["object"].id
        user_posts = Post.objects.filter(user_id=user_pk, is_active=True).order_by('-created_date')
        ctx['posts'] = user_posts
        return ctx


def profile(request, pk):
    user = get_object_or_404(BlogUser, pk=pk)
    user_posts = Post.objects.filter(user_id=user.id, is_active=True).order_by('-created_date')
    print(f'111111111111   {user_posts}')

    if request.method == 'POST':
        # ???????? ???????????? ?????????????? ???????????????? ????????????????????????
        if '/auth/profile_banned/' in request.path:
            banned_form = BannedForm(request.POST)
            if banned_form.is_valid():
                user.is_banned = 1
                user.banned_time = banned_form['banned_time'].value()
                user.start_banned_time = datetime.date.today()
                user.stop_banned_time = user.start_banned_time + datetime.timedelta(days=int(user.banned_time))
                user.save()
    else:
        # ???????? ?????????????? ???????????? ????????????????
        banned_form = BannedForm()
        
        # ?????? ?????????????? ?????????? ????????????????????
        if '/auth/profile_activate/' in request.path:
            user.is_banned = 0
            user.banned_time = 0
            user.start_banned_time = None
            user.stop_banned_time = None
            user.save()
            banned_form = BannedForm()
        # ?????????????? ???????? ????????????????????
        if '/auth/profile_moderator_on/' in request.path:
            user.is_moderator = True
            user.save()
        # ?????????????? ???????????? ????????????????????
        if '/auth/profile_moderator_off/' in request.path:
            user.is_moderator = False
            user.save()

    content = {
        'title': '?????????????? ????????????????????????',
        'user_read': user,
        'banned_form': banned_form,
        'posts': user_posts,
    }
    return render(request, 'authapp/profile.html', content)


def delete_notification(request, pk):
    notification = Notification.objects.get(id=pk)
    notification.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
