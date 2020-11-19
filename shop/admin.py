from django.contrib import admin

# Register your models here.
from . models import Product , contact , Orders, OrderUpdate
admin.site.register(Product)
admin.site.register(contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)