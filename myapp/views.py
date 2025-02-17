from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Category, Product

# Updated index view using index.html (inherits from base.html)
def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'cat_list': cat_list})

# Updated about view using about.html template
def about(request):
    return render(request, 'myapp/about.html')

# Updated detail view using detail.html template
def detail(request, cat_no):
    category = get_object_or_404(Category, id=cat_no)
    products = Product.objects.filter(category=category)
    context = {'category': category, 'products': products}
    return render(request, 'myapp/detail.html', context)
