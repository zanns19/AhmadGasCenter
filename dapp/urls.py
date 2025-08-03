from django.contrib import admin
from django.urls import path , include
from dapp import views
urlpatterns = [
    path("", views.index, name="index" ),
    path("about", views.about, name="about" ),
    path("contact", views.contact, name="contact" ),
    path("services", views.services, name="services" ),
    path("discounts/", views.discounts, name="discounts" ),
    path("search/", views.search, name="Search" ),
    path("products/<str:type>/<int:id>/", views.products, name="products"),
    


]
