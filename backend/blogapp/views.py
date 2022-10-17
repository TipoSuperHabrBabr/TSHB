from django.shortcuts import render


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
