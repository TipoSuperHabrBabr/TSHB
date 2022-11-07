from authapp.models import BlogUser
from blogapp.forms import CommentForm, PostForm
from blogapp.models import Post, Like, Comment, Notification
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView


def index(request):
    posts_list = Post.objects.all().filter(is_active=True).order_by('-created_date')

    tags_str = ''
    if posts_list:
        for post in posts_list:
            tags_str = f'{tags_str} {post.tags}'
        tags_list = list(set(tags_str.split()))[:10]
    else:
        tags_list = ''

    new_posts_list = posts_list[0:2]
    old_posts_list = posts_list[2:]
    paginator = Paginator(old_posts_list, 9)

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
                      'tags': tags_list,
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
    posts_list = Post.objects.filter(category=current_category, is_active=True).order_by('-created_date')
    paginator = Paginator(posts_list, 6)

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
    tags = post_id.tags.split()
    comments = Comment.objects.filter(post_id=pk, is_active=True).order_by('-parent_comment_id')
    user_id = request.user
    new_comment = None
    model_type_posts = ContentType.objects.get_for_model(Post)
    model_type_commets = ContentType.objects.get_for_model(Comment)
    like_posts = Like.objects.filter(content_type=model_type_posts, object_id=pk, liked=True)
    like_commets = Like.objects.filter(content_type=model_type_commets, parent_object=pk, liked=True)

    path = request.build_absolute_uri()

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.save(commit=True)
            # считываем только что сохраненный комментарий
            comment = Comment.objects.get(parent_comment_id=0)
            # и записываем собственный id как родительский
            comment.parent_comment_id = comment.id
            comment.save()
            notification_to_moderator(comment.body_text, request)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        comment_form = CommentForm(initial={'user_id': user_id, 'post_id': post_id, })

    return render(request, 'blogapp/blog-post.html',
                  {'post': post_id,
                   'tags': tags,
                   'user_id': user_id,
                   'comments': comments,
                   'new_comment': new_comment,
                   'form': comment_form,
                   'like_posts': like_posts,
                   'like_commets': like_commets,
                   'path': path,
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
        context_data['user_id'] = user_id
        context_data['form'] = PostForm(initial={'user_id': user_id})
        return context_data

    def get_success_url(self, **kwargs):
        return reverse('index')


@login_required
def edit_post(request, pk):
    post = Post.objects.get(id=pk)

    # проверяем права юзера и статус поста
    if request.user == post.user_id or request.user.is_moderator or request.user.is_superuser and post.is_active:

        if request.method == 'POST':

            form = PostForm(request.POST, request.FILES or None, instance=post)
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

    return HttpResponseForbidden('Permission Error')


@login_required
def delete_post(request, pk):
    post = Post.objects.get(id=pk)

    if request.user == post.user_id or request.user.is_moderator or request.user.is_superuser and post.is_active:
        if request.method == "POST":
            post.delete()
            return HttpResponseRedirect(reverse('index'))

        context = {
            'object': post,
            'user': request.user
        }
        return render(request, 'blogapp/post_confirm_delete.html', context)

    return HttpResponseForbidden('Permission Error')


@login_required
def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user == comment.user_id or request.user.is_moderator or request.user.is_superuser and comment.is_active:
        if comment.head_comment:
            # при удалении головного комментария удаляем его и все подкомментарии
            comments = Comment.objects.filter(parent_comment_id=pk)
            for comment in comments:
                comment.delete()
        else:
            # иначе удалем только один подкомментарий
            comment.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # selected_comment = get_object_or_404(Comment, id=pk)
    # selected_comment.delete()


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
        notification_to_moderator(comment_new.body_text, request)
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
        text = self.request.POST["body_text"]
        notification_to_moderator(text, self.request)
        return reverse('blogapp:read_post', kwargs=dict(pk=self.kwargs['pkp']))


@login_required
def like(request, obj, pk, pkc):
    user = request.user
    obj = globals().get(obj)
    model_type = ContentType.objects.get_for_model(model=obj)
    try:
        like = Like.objects.get(content_type=model_type, object_id=pkc, parent_object=pk, user_id=user)
        like.delete()
    except:
        Like.objects.create(content_type=model_type, object_id=pkc, user_id=user, parent_object=pk, liked=True)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def notification_to_moderator(text, request):
    if text.find('@moderator') != -1:
        print(f'1111111 {request.build_absolute_uri()}')
        path = request.build_absolute_uri()
        notification = Notification()
        notification.path = path
        notification.body_text = text
        notification.save()
