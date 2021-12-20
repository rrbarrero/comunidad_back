from django.shortcuts import render
from django.shortcuts import get_object_or_404
from blog.models import Articulo

def home(request):
    return render(request, 'maqueta.html', {
        'articulos': Articulo.objects.all().order_by('-fecha_creacion')
    })

def detail(request, id):
    articulo = get_object_or_404(Articulo, pk=id)
    return render(request, 'detalle.html', {
        'articulo': articulo
    })