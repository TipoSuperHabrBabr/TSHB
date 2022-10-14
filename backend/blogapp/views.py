from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'blogapp/index.html',
                  context={'title': 'TipoSuperHabrBabr'}
                  )


def blog(request):
    return render(request, 'blogapp/blog.html')
