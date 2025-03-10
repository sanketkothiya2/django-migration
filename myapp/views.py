from datetime import date, datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse  # Added HttpResponse here
from django.urls import reverse
from .forms import OrderForm, InterestForm
from .models import Category, Product, Client, Order

def index(request):
    cat_list = Category.objects.only('id', 'name').order_by('id')[:10]
    # Check session for last_login
    last_login = request.session.get('last_login', None)
    if last_login:
        message = f"Last login: {last_login}"
    else:
        message = "Your last login was more than one hour ago."
    return render(request, 'myapp/index.html', {'cat_list': cat_list, 'message': message})

def about(request):
    # Check for 'about_visits' cookie
    about_visits = request.COOKIES.get('about_visits', 0)
    try:
        about_visits = int(about_visits) + 1
    except ValueError:
        about_visits = 1
    response = render(request, 'myapp/about.html', {'about_visits': about_visits})
    # Set cookie to expire in 5 minutes (300 seconds)
    response.set_cookie('about_visits', about_visits, max_age=300)
    return response

def detail(request, cat_no):
    category = get_object_or_404(Category, id=cat_no)
    products = category.products.all()
    if not products:
        messages.warning(request, "No products available in this category.")
    return render(request, 'myapp/detail.html', {'category': category, 'products': products})

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
                order.product.stock -= order.num_units
                order.product.save()
                order.client = request.user.client  # Set the client to the logged-in user
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

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                # Store login time in session and set expiry to 1 hour (3600 seconds)
                request.session['last_login'] = str(datetime.now())
                request.session.set_expiry(3600)
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
    return HttpResponseRedirect(reverse('myapp:index'))

@login_required
def mvorders(request):
    try:
        client = request.user.client
        orders = Order.objects.filter(client=client)
        if orders:
            return render(request, 'myapp/mvorders.html', {'orders': orders})
        else:
            return render(request, 'myapp/mvorders.html', {'message': 'You have not placed any orders.'})
    except Client.DoesNotExist:
        return render(request, 'myapp/mvorders.html', {'message': 'You are not a registered client!'})