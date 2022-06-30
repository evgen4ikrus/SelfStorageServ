from django.shortcuts import render
from cloudipsp import Api, Checkout
from django.shortcuts import redirect


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
