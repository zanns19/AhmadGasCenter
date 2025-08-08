from django.shortcuts import render ,HttpResponse
from .models import Product , Kitchen_Items , Contact , Discount,KitchenCategory

from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
   
# Create your views here.
def index(request):
    products = Product.objects.all()
    kitchens = Kitchen_Items.objects.all()
    discounts = Discount.objects.all()

    selected_discounts = []
    total = discounts.count()

    
    if total >= 2:
         selected_discounts.append({"item": discounts[0], "label": "In Stock", "class": "first"})
         selected_discounts.append({"item": discounts[1], "label": "In Stock", "class": "second"})
         if total > 3:
             selected_discounts.append({"item": discounts[total - 2], "label": "New", "class": "second-last"})
             selected_discounts.append({"item": discounts[total - 1], "label": "New", "class": "last"})


    params = {
        'product': products,
        'kitchen': kitchens,
        'discount': selected_discounts
    }
    return render(request, 'index.html', params)

def discounts(request):
    discounts=Discount.objects.all()
    params={'discount':discounts}
    return render(request,'discount.html',params)
def services(request):
    # products= Product.objects.all()
    # paginator=Paginator(products,2)
    # page_number=request.GET.get('page')
    # Product_dataFinal=paginator.get_page(page_number)
    # kitchens=Kitchen_Items.objects.all()
    # # allprods=[[products],[kitchens]]
    # n=len(products)
    # params={'product':Product_dataFinal,'kitchen':kitchens}
# Gas Products Pagination
    gas_products = Product.objects.all()
    gas_paginator = Paginator(gas_products, 12)  # Show 12 gas products per page
    gas_page_number = request.GET.get('gas_page')
    gas_page_obj = gas_paginator.get_page(gas_page_number)

    # Kitchen Items Pagination
    kitchen_items = Kitchen_Items.objects.all()
    kitchen_paginator = Paginator(kitchen_items, 12)  # Show 12 kitchen items per page
    kitchen_page_number = request.GET.get('kitchen_page')
    kitchen_page_obj = kitchen_paginator.get_page(kitchen_page_number)
    categories = KitchenCategory.objects.prefetch_related('kitchen_items').all()
    


    context = {
        'product': gas_page_obj,
        'kitchen': kitchen_page_obj,
        'categories': categories
    }

    return render(request,'services.html',context)
def searchMatch(query,item):
        return query.lower() in item.desc.lower() or query.lower() in item.product_name.lower()
def search(request):
    query = request.GET.get('search', '').strip()
    category = request.GET.get('category', 'all')

    products = []
    kitchens = []

    category_display = {
        'all': 'All Categories',
        'kitchen': 'Kitchen Appliances',
        'gas': 'Camping Stoves',
        'hood': 'Hood',
        'built': 'Built-In',
        'stove': 'Stove'
    }

    category_label = category_display.get(category, 'All Categories')

    if category == 'gas':
        products = Product.objects.filter(Q(product_name__icontains=query) | Q(desc__icontains=query))
    elif category in ['hood', 'built', 'stove']:
        kitchens = Kitchen_Items.objects.filter(
            Q(product_name__icontains=query) | Q(desc__icontains=query),
            category__name__iexact=category
        )
    elif category == 'kitchen':
        kitchens = Kitchen_Items.objects.filter(Q(product_name__icontains=query) | Q(desc__icontains=query))
    else:
        products = Product.objects.filter(Q(product_name__icontains=query) | Q(desc__icontains=query))
        kitchens = Kitchen_Items.objects.filter(Q(product_name__icontains=query) | Q(desc__icontains=query))

    return render(request, 'services.html', {
        'product': products,
        'kitchen': kitchens,
        'query': query,
        'category_label': category_label,
    })


# Create your views here.
def about(request):
    return render(request,'about.html')
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        _subject=request.POST.get('_subject','')
        message=request.POST.get('message','')
        contact = Contact(name=name,email=email,_subject=_subject,message=message)
        contact.save()
        # Prepare email
        subject = f"New Contact Form Submission: {_subject}"
        full_message = f"""
        You have a new message from Ahmad Gas Center Contact Form:

        Name: {name}
        Email: {email}
        Subject: {_subject}

        Message:
        {message}
        """

        # Send email to owner
        send_mail(
            subject,
            full_message,
            settings.DEFAULT_FROM_EMAIL,       # From (you must configure this in settings.py)
            [settings.CONTACT_RECEIVER_EMAIL], # To (owner email from settings)
            fail_silently=False,
        )
    return render(request,'contact.html')
def products(request, type, id):
    item = None

    if type in ["product", "products"]:
        item = Product.objects.filter(id=id).first()
    elif type in ["kitchen", "kitchens"]:
        item = Kitchen_Items.objects.filter(id=id).first()
    elif type in ["discount", "discounts"]:
        item = Discount.objects.filter(id=id).first()

    if not item:
        return HttpResponse(f"{type.capitalize()} item not found", status=404)

    return render(request, 'products.html', {'item': item})
