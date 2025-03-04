from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import OrderForm, InterestForm
from .models import Category
from .models import Product

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

def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})


def place_order(request):
    msg = ''
    prodlist = Product.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if order.num_units <= order.product.stock:
                # Update the stock
                order.product.stock -= order.num_units
                order.product.save()

                # Set the order date and save
                order.status_date = date.today()
                order.save()

                msg = 'Your order has been placed successfully.'
            else:
                msg = 'We do not have sufficient stock to fill your order.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()

    return render(request, 'myapp/placeorder.html', {
        'form': form,
        'msg': msg,
        'prodlist': prodlist
    })


def productdetail(request, prod_id):
    product = get_object_or_404(Product, pk=prod_id)

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if int(form.cleaned_data['interested']) == 1:
                product.interested += 1
                product.save()
                return redirect('myapp:index')
    else:
        form = InterestForm()

    return render(request, 'myapp/productdetail.html', {
        'product': product,
        'form': form,
    })