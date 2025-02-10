from django.core.management.base import BaseCommand
from myapp.models import Product, Category, Client, Order

class Command(BaseCommand):
    help = "Run database queries and display results"

    def handle(self, *args, **kwargs):
        # Query a: List all products
        products = Product.objects.all()
        print("\nAll Products:")
        for product in products:
            print(product)

        #
        # # Query b: List all clients
        # clients = Client.objects.all()
        # print("\nAll Clients:")
        # for client in clients:
        #     print(client)

        non_ontario_clients = Client.objects.filter(province='ON')
        for client in non_ontario_clients:
            print(client)

        #
        # # Query c: List all orders
        # orders = Order.objects.all()
        # print("\nAll Orders:")
        # for order in orders:
        #     print(order)
        #
        # # Query d: Clients with last name 'Jones'
        # jones_clients = Client.objects.filter(last_name='Jones')
        # print("\nClients with last name 'Jones':")
        # for client in jones_clients:
        #     print(client)
        #
        # # Query e: Products in category 'Furniture'
        # furniture_products = Product.objects.filter(category__name='Furniture')
        # print("\nFurniture Products:")
        # for product in furniture_products:
        #     print(product)
        #
        # # Query f: Clients living on 'King Street'
        # king_street_clients = Client.objects.filter(shipping_address__icontains='King Street')
        # print("\nClients on King Street:")
        # for client in king_street_clients:
        #     print(client)
        #
        # # Query g: Clients living on an 'Avenue' and in Quebec
        # avenue_clients = Client.objects.filter(shipping_address__icontains='Avenue', province='QC')
        # print("\nClients on Avenue in Quebec:")
        # for client in avenue_clients:
        #     print(client)
        #
        # # Query h: Clients interested in 'Home Decor'
        # home_decor_clients = Client.objects.filter(interested_in__name='Home Decor')
        # print("\nClients interested in Home Decor:")
        # for client in home_decor_clients:
        #     print(client)
        #
        # # Query i: Products costing more than $1000
        # expensive_products = Product.objects.filter(price__gt=1000)
        # print("\nProducts costing more than $1000:")
        # for product in expensive_products:
        #     print(product)
        #
        # # Query j: Clients not living in Ontario
        # non_ontario_clients = Client.objects.exclude(province='ON')
        # print("\nClients not living in Ontario:")
        # for client in non_ontario_clients:
        #     print(client)
        #
        # # Query k: Orders placed by 'Mary'
        # mary_orders = Order.objects.filter(client__first_name='Mary')
        # print("\nOrders placed by Mary:")
        # for order in mary_orders:
        #     print(order)
        #
        # # Query l: Products not available
        # unavailable_products = Product.objects.filter(available=False)
        # print("\nUnavailable Products:")
        # for product in unavailable_products:
        #     print(product)
        #
        # # Query m: Products with stock between 60 and 110
        # stock_products = Product.objects.filter(stock__range=(60, 110))
        # print("\nProducts with stock between 60 and 110:")
        # for product in stock_products:
        #     print(product)
        #
        # # Query n: Get the first name of the client of Order with pk=1
        # order = Order.objects.get(pk=1)
        # print("\nClient of Order 1:", order.client.first_name)
        #
        # # Query o: Categories the client 'john' is interested in
        # john = Client.objects.get(username='john')
        # john_categories = john.interested_in.all()
        # print("\nCategories John is interested in:")
        # for category in john_categories:
        #     print(category)
        #
        # # Query p: Products with price > $500 and stock < 100
        # specific_products = Product.objects.filter(price__gt=500, stock__lt=100)
        # print("\nProducts with price > $500 and stock < 100:")
        # for product in specific_products:
        #     print(product)
        #
        # # Query q: Warehouse location of the category that 'bill' is interested in
        # bill = Client.objects.get(username='bill')
        # bill_category = bill.interested_in.first()
        # print("\nWarehouse location for Bill's category:", bill_category.warehouse)
        #
        # # Query r: Categories the client who ordered a 'TV' is interested in
        # tv_order = Order.objects.get(product__name='TV')
        # tv_client_categories = tv_order.client.interested_in.all()
        # print("\nCategories of the client who ordered a TV:")
        # for category in tv_client_categories:
        #     print(category)
        #
        #
