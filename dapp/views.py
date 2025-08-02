from django.shortcuts import render ,HttpResponse
from .models import Product , Kitchen_Items , Contact
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.
def index(request):
    products= Product.objects.all()
    kitchens=Kitchen_Items.objects.all()
    # allprods=[[products],[kitchens]]
    n=len(products)
    params={'product':products,'kitchen':kitchens}
    return render(request,'index.html',params)
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
    gas_paginator = Paginator(gas_products, 4)  # Show 4 gas products per page
    gas_page_number = request.GET.get('gas_page')
    gas_page_obj = gas_paginator.get_page(gas_page_number)

    # Kitchen Items Pagination
    kitchen_items = Kitchen_Items.objects.all()
    kitchen_paginator = Paginator(kitchen_items, 8)  # Show 4 kitchen items per page
    kitchen_page_number = request.GET.get('kitchen_page')
    kitchen_page_obj = kitchen_paginator.get_page(kitchen_page_number)

    context = {
        'product': gas_page_obj,
        'kitchen': kitchen_page_obj,
    }

    return render(request,'services.html',context)
def searchMatch(query,item):
        return query.lower() in item.desc.lower() or query.lower() in item.product_name.lower()
def search(request):
    query = request.GET.get('search', '').strip()
    category = request.GET.get('category', 'all')

    products = []
    kitchens = []

    # Mapping for display
    category_display = {
        'all': 'All Categories',
        'gas': 'Gas Items',
        'kitchen': 'Kitchen Items'
    }

    category_label = category_display.get(category, 'All Categories')

    if query:
        if category == "gas":
            products = Product.objects.filter(
                Q(product_name__icontains=query) | Q(desc__icontains=query)
            )
        elif category == "kitchen":
            kitchens = Kitchen_Items.objects.filter(
                Q(product_name__icontains=query) | Q(desc__icontains=query)
            )
        else:
            products = Product.objects.filter(
                Q(product_name__icontains=query) | Q(desc__icontains=query)
            )
            kitchens = Kitchen_Items.objects.filter(
                Q(product_name__icontains=query) | Q(desc__icontains=query)
            )

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
    if type == "product":
        try:
            item = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return HttpResponse("Product not found", status=404)
    elif type == "kitchen":
        try:
            item = Kitchen_Items.objects.get(id=id)
        except Kitchen_Items.DoesNotExist:
            return HttpResponse("Kitchen item not found", status=404)
    else:
        return HttpResponse("Invalid type", status=400)

    return render(request, 'products.html', {'item': item})
