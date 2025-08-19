from django.contrib import admin
from .models import Product , Kitchen_Items , Contact, Discount , Kitchen_Items, KitchenCategory,Instant_Gyser,Regulator,Valves,Accessories,Offermsg


# Register your models here.
admin.site.site_header="AHMAD HASSAN MUFTI"
admin.site.site_title="AHMAD GAS CENTER"
admin.site.index_title="Admin"
admin.site.register(Product),
admin.site.register(Kitchen_Items),
admin.site.register(KitchenCategory),
admin.site.register(Contact),
admin.site.register(Discount),
admin.site.register(Instant_Gyser),
admin.site.register(Regulator),
admin.site.register(Valves),
admin.site.register(Accessories),
admin.site.register(Offermsg)
