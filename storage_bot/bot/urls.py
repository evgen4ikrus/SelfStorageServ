from django.urls import path
from .views import pay_cell

urlpatterns = [
    path('', pay_cell),
]