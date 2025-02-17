from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import Category

def index(request):
    cat_list = Category.objects.only('id', 'name').order_by('id')[:10]
    return render(request, 'myapp/index.html', {'cat_list': cat_list})

def about(request):
    return render(request, 'myapp/about.html')

def detail(request, cat_no):
    category = get_object_or_404(Category, id=cat_no)
    products = category.products.all()

    if not products:
        messages.warning(request, "No products available in this category.")

    return render(request, 'myapp/detail.html', {'category': category, 'products': products})
