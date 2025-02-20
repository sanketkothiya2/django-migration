from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Category, Product

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    product_list = Product.objects.all().order_by('-price')[:5]
    context = {
        'categories': cat_list,
        'products': product_list
    }
    return render(request, 'myapp/index.html', context)

def about(request):
    return HttpResponse("This is an Online Store APP.")

def detail(request, cat_no):
    category = get_object_or_404(Category, id=cat_no)

    category = Category.objects.filter(id=cat_no).first()  # Ensures category is always defined

    # Check if category exists before using it
    if category is None:
        return HttpResponse("<h1>Category not found</h1>")  # Instead of 404, show a message

    # Retrieve all products that belong to the selected category
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,


    }
    print(context)
    return render(request, 'myapp/detail.html', context)