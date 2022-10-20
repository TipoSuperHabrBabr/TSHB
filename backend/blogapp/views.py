from authapp.models import BlogUser
from blogapp.forms import PostForm
from blogapp.models import Post
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView


# Create your views here.
def index(request):
    return render(request, 'blogapp/index.html',
                  context={'title': 'TipoSuperHabrBabr'}
                  )


def blog(request):
    categories = {
        '0': 'Все категории',
        '1': 'Дизайн',
        '2': 'Веб-разработка',
        '3': 'Мобильная разработка',
        '4': 'Маркетинг'
    }
    category_id = request.GET.get('id')
    current_category = categories[category_id]
    context = {
        'categories': categories,
        'current_category': current_category,
        'title': current_category,
    }

    return render(request, 'blogapp/blog.html', context)


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
    print(request.user != post.user_id)
    print(post.is_active == True)
    if request.user != post.user_id or post.is_active is not True:  # проверяем доступ юзера и статус поста
        return HttpResponseForbidden('Permission Error')

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


@login_required
def delete_post(request, pk):
    post = Post.objects.get(id=pk)

    if request.user != post.user_id or post.is_active is not True:  # проверяем доступ юзера и статус поста
        return HttpResponseForbidden('Permission Error')

    if request.method == "POST":
        post.delete()
        return HttpResponseRedirect(reverse('index'))

    context = {'object': post}
    return render(request, 'blogapp/post_confirm_delete.html', context)
