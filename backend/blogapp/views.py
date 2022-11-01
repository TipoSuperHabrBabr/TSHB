from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from authapp.models import BlogUser
from blogapp.forms import CommentForm
from blogapp.forms import PostForm
from blogapp.models import Comment
from blogapp.models import Post
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView


def index(request):
    posts_list = Post.objects.all().order_by('-created_date')
    new_posts_list = Post.objects.all().order_by('-created_date')[0:2]
    old_posts_list = Post.objects.all().order_by('-created_date')[2:]
    paginator = Paginator(old_posts_list, 6)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)


    return render(request, 'blogapp/index.html',
                  context={
                      'title': 'TipoSuperHabrBabr',
                      'posts_list': posts_list,
                      'new_posts_list': new_posts_list,
                      'old_posts_list': page_obj,
                  },
                  )


def blog(request):
    categories = {
        '0': 'ALL',
        '1': 'DESING',
        '2': 'WEB_DEVELOPMENT',
        '3': 'MOBIL_DEVELOPMENT',
        '4': 'MARKETING'
    }
    category_id = request.GET.get('id')
    current_category = categories[category_id]
    posts_list = Post.objects.filter(category=current_category).order_by('-created_date')
    paginator = Paginator(posts_list, 2)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'current_category': current_category,
        'title': current_category,
        'posts_list': page_obj,
        'category_id': category_id,
    }
    return render(request, 'blogapp/blog.html', context)


def post_detail(request, pk):
    post_id = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post_id=pk, is_active=True).order_by('parent_comment_id')
    user_id = request.user
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.save(commit=True)
            # считываем только что сохраненный комментарий
            comment = Comment.objects.get(parent_comment_id=0)
            # и записываем собственный id как родительский
            comment.parent_comment_id = comment.id
            comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        comment_form = CommentForm(initial={'user_id': user_id, 'post_id': post_id, })

    return render(request,
                  'blogapp/blog-post.html',
                  {'post': post_id,
                   'user_id': user_id,
                   'comments': comments,
                   'new_comment': new_comment,
                   'form': comment_form,
                   }
                  )


@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    model = Post
    fields = '__all__'
    template_name = 'blogapp/create_post.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        user = self.request.user
        user_id = get_object_or_404(BlogUser, username=user).id
        context_data['user'] = user
        context_data['user_id '] = user_id
        context_data['form'] = PostForm(initial={'user_id': user_id})
        return context_data

    def get_success_url(self, **kwargs):
        return reverse('index')


@login_required
def edit_post(request, pk):
    post = Post.objects.get(id=pk)
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
        'user': request.user
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

    context = {
        'object': post,
        'user': request.user
    }
    return render(request, 'blogapp/post_confirm_delete.html', context)


@login_required
def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.user_id or comment.is_active is not True:  # проверяем доступ юзера и статус поста
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # selected_comment = get_object_or_404(Comment, id=pk)
    # selected_comment.delete()

    if comment.head_comment:
        # при удалении головного комментария удаляем его и все подкомментарии
        comments = Comment.objects.filter(parent_comment_id=pk)
        for comment in comments:
            comment.delete()
    else:
        # иначе удалем только один подкомментарий
        comment.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def comment_reply(request, pk):
    user = request.user
    comment = Comment.objects.get(id=pk)
    reply_form = CommentForm

    if request.method == "POST":
        # считываем форму
        reply_form = CommentForm(data=request.POST)

        # формируем подкомментарий
        comment_new = Comment()
        comment_new.post_id = comment.post_id
        comment_new.user_id = user
        comment_new.body_text = reply_form['body_text'].value()
        comment_new.parent_comment_id = comment.id
        comment_new.head_comment = False
        comment_new.save()
        # возвращаемся на страницу описания блога с комментариями
        return HttpResponseRedirect(f'/blog/read_post/{comment.post_id.id}/')

    context = {
        'comment': comment,
        'form': reply_form,
        'user': user,
    }
    return render(request, 'blogapp/comment_reply.html', context)



@method_decorator(login_required, name='dispatch')
class CommentUpdateView(UpdateView):
    model = Comment
    fields = ["body_text"]
    template_name = 'blogapp/edit_comment.html'

    def get_success_url(self, **kwargs):
        # print(self.kwargs['pk'])
        return reverse('blogapp:read_post', kwargs=dict(pk=self.kwargs['pkp']))
