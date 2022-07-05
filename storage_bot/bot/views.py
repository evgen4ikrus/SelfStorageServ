from django.shortcuts import render
from cloudipsp import Api, Checkout
from django.shortcuts import redirect
from bot.models import Order, User, Storage


def pay_cell(request):
    api = Api(merchant_id=1396424,
            secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": 10000
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


def orders_view(request):
    active_orders = Order.objects.all()
    storages = Storage.objects.all().prefetch_related('cells')
    context = {
        'active_orders': active_orders,
        'storages': storages,
    }
    return render(request, 'active_orders.html', context)


def user_view(request, userid):
    user = User.objects.filter(id=userid).get()
    context = {
        'user': user,
    }
    return render(request, 'user_info.html', context)

def storage_view(request, storageid):
    storage = Storage.objects.filter(id=storageid).prefetch_related("cells").get()
    context = {
        'storage': storage,
        'cells': storage.cells.all(),
    }
    return render(request, 'storage.html', context)
