from django.contrib import admin
from bot.models import *

@admin.register(User)
class AdminUser(admin.ModelAdmin):
    pass

@admin.register(Cell)
class AdminBox(admin.ModelAdmin):
    pass

@admin.register(Storage)
class AdminStorage(admin.ModelAdmin):
    pass

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    pass
