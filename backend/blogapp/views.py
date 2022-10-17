from authapp.models import BlogUser
from blogapp.forms import PostForm
from blogapp.models import Post
from django import http
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView


# Create your views here.
def index(request):
    return render(request, 'index.html')


def error_user(request):
    return render(request, 'blogapp/error_user.html')


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = '__all__'
    template_name = 'blogapp/create_post.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        user_id = get_object_or_404(BlogUser, username=user).id
        context_data['user_id '] = user_id
        context_data['form'] = PostForm(initial={'user_id': user_id})
        return context_data

    def get_success_url(self, **kwargs):
        return reverse('index')

@login_required
def edit_post(request, pk):
    post = Post.objects.get(id=pk)

    if request.user == post.user_id: # проверяем соответствие юзера из поста и реквеста
        if request.method == 'POST':

            form = PostForm(request.POST or None, instance=post)
            if form.is_valid():
                form.save()
                post.edit_date = timezone.now()
                post.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            form = PostForm(request.POST or None, instance=post)

        content = {
            'title': 'Редактирование статьи',
            'form': form,
            'post': post,
        }
        return render(request, 'blogapp/edit_post.html', content)

    else:
        return HttpResponseForbidden('Permission Error')

@login_required
def delete_post(request, pk):
    post = Post.objects.get(id=pk)

    if request.user == post.user_id:  # проверяем соответствие юзера из поста и реквеста
        if request.method == "POST":
            post.delete()
            return HttpResponseRedirect(reverse('index'))

        context = {'object': post}
        return render(request, 'blogapp/post_confirm_delete.html', context)

    else:
        return HttpResponseForbidden('Permission Error')


