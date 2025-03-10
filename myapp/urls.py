from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),  # Default to login
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('about/', views.about, name='about'),
    path('myorders/', views.myorders, name='myorders'),
    path('category/<int:cat_no>/', views.detail, name='detail'),
    path('products/', views.products, name='products'),
    path('place_order/', views.place_order, name='place_order'),
    path('products/<int:prod_id>/', views.productdetail, name='productdetail'),
]