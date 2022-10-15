from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'blogapp/index.html',
                  context={'title': 'TipoSuperHabrBabr'}
                  )


def blog(request, pk=None):
    category = {0: 'Все',
                1: 'Дизайн',
                2: 'Веб-разработка',
                3: 'Мобильная разработка',
                4: 'Маркетинг'}

    return render(request, 'blogapp/blog.html',
                  context={'category': category})
