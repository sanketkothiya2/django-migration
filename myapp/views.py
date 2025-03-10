from datetime import date, datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms
from .models import Order
from datetime import datetime

from .forms import OrderForm, InterestForm
from .models import Category, Product

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('myapp:index')
    else:
        form = UserForm()
    return render(request, 'myapp/register.html', {'form': form})

@login_required
def myorders(request):
    if hasattr(request.user, 'client'):
        orders = Order.objects.filter(client=request.user.client)
        return render(request, 'myapp/myorders.html', {'orders': orders})
    else:
        return render(request, 'myapp/myorders.html', {'message': 'You are not a registered client!'})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                request.session['last_login'] = str(datetime.now())
                request.session.set_expiry(3600)  # 1 hour
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    request.session['last_login'] = None
    return HttpResponseRedirect(reverse('myapp:login'))

@login_required
def index(request):
    cat_list = Category.objects.only('id', 'name').order_by('id')[:10]
    last_login_raw = request.session.get('last_login')
    last_login = datetime.strptime(last_login_raw, '%Y-%m-%d %H:%M:%S.%f').strftime('%B %d, %Y at %I:%M %p') if last_login_raw else 'Your last login was more than one hour ago.'
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'last_login': last_login})

@login_required
def about(request):
    visits = int(request.COOKIES.get('about_visits', '0')) + 1
    response = render(request, 'myapp/about.html', {'visits': visits})
    response.set_cookie('about_visits', visits, max_age=300)  # 5 minutes
    return response

@login_required
def detail(request, cat_no):
    category = get_object_or_404(Category, id=cat_no)
    products = category.products.all()

    if not products:
        messages.warning(request, "No products available in this category.")

    return render(request, 'myapp/detail.html', {'category': category, 'products': products})

@login_required
def products(request):
    prodlist = Product.objects.all().order_by('id')[:10]
    return render(request, 'myapp/products.html', {'prodlist': prodlist})

@login_required
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

@login_required
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