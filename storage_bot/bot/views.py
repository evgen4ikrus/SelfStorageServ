from django.shortcuts import render
from cloudipsp import Api, Checkout
from django.shortcuts import redirect
from bot.models import Order, User


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
    context = {
        'active_orders': active_orders,
    }
    return render(request, 'active_orders.html', context)


def user_view(request, userid):
    user = User.objects.filter(id=userid).get()
    context = {
        'user': user,
    }
    return render(request, 'user_info.html', context)
