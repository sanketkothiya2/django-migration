from django.core.management.base import BaseCommand
from myapp.models import Category, Product, Client, Order
from django.contrib.auth.models import User
from datetime import date

class Command(BaseCommand):
    help = 'Populate the database with initial data'

    def handle(self, *args, **kwargs):
        # Create Categories
        furniture = Category.objects.create(name='Furniture', warehouse='Windsor')
        appliances = Category.objects.create(name='Appliances', warehouse='Windsor')
        electronics = Category.objects.create(name='Electronics', warehouse='London')
        home_decor = Category.objects.create(name='Home Decor', warehouse='Waterloo')
        flooring = Category.objects.create(name='Flooring', warehouse='London')

        # Create Clients
        john = Client.objects.create_user(username='john', password='john', first_name='John', last_name='Smith', shipping_address='123 University Avenue', city='Windsor', province='ON')
        mary = Client.objects.create_user(username='mary', password='mary', first_name='Mary', last_name='Hall', shipping_address='456 Sunset Avenue', city='Windsor', province='ON')
        alan = Client.objects.create_user(username='alan', password='alan', first_name='Alan', last_name='Jones', shipping_address='789 King Street', city='Calgary', province='AB')
        josh = Client.objects.create_user(username='josh', password='josh', first_name='Josh', last_name='Jones', shipping_address='456 Sunset Avenue', city='Montreal', province='QC')
        bill = Client.objects.create_user(username='bill', password='bill', first_name='Bill', last_name='Wang', shipping_address='987 King Street', city='Edmonton', province='AB')

        # Set interests for clients
        john.interested_in.set([furniture, appliances, electronics, home_decor])
        mary.interested_in.set([furniture, electronics])
        alan.interested_in.set([appliances, electronics, home_decor])
        josh.interested_in.set([furniture, home_decor])
        bill.interested_in.set([electronics])

        # Create Products
        Product.objects.create(category=home_decor, name='Clock', price=99.99, stock=50, available=True)
        Product.objects.create(category=home_decor, name='Vase', price=82.54, stock=100, available=True)
        Product.objects.create(category=home_decor, name='Painting', price=135.80, stock=80, available=True)
        Product.objects.create(category=home_decor, name='Lamp', price=59.99, stock=200, available=True)
        Product.objects.create(category=electronics, name='Tablet', price=299.99, stock=0, available=False)
        Product.objects.create(category=electronics, name='Laptop', price=975.50, stock=85, available=True)
        Product.objects.create(category=electronics, name='TV', price=3500.00, stock=20, available=True)
        Product.objects.create(category=furniture, name='Table', price=599.99, stock=120, available=True)
        Product.objects.create(category=furniture, name='Dresser', price=360.85, stock=100, available=True)
        Product.objects.create(category=furniture, name='Bed', price=1225.25, stock=0, available=False)
        Product.objects.create(category=furniture, name='Sofa', price=1500.95, stock=175, available=True)
        Product.objects.create(category=appliances, name='Dryer', price=775.00, stock=0, available=False)
        Product.objects.create(category=appliances, name='Washer', price=885.75, stock=50, available=True)
        Product.objects.create(category=appliances, name='Stove', price=950.50, stock=50, available=True)

        # Create Orders
        Order.objects.create(product=Product.objects.get(name='Lamp'), client=mary, num_units=2, status_date=date.today())
        Order.objects.create(product=Product.objects.get(name='TV'), client=john, num_units=1, status_date=date.today())

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with initial data'))