from django.contrib import admin
from .models import Product , Kitchen_Items , Contact

# Register your models here.
admin.site.site_header="AHMAD HASSAN MUFTI"
admin.site.site_title="AHMAD GAS CENTER"
admin.site.index_title="Admin"
admin.site.register(Product),
admin.site.register(Kitchen_Items),
admin.site.register(Contact)
