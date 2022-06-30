from django.contrib import admin
from bot.models import User, Box, Storage, Order

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    pass

@admin.register(Box)
class AdminBox(admin.ModelAdmin):
    pass

@admin.register(Storage)
class AdminStorage(admin.ModelAdmin):
    pass

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    pass