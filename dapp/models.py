from django.db import models

# Create your models here.
class Kitchen_Items(models.Model):
    product_id =models.AutoField
    product_name=models.CharField(max_length=120,default="")
    desc=models.CharField(max_length=1020,default="")
    price=models.IntegerField(default=0)
    rating=models.FloatField(default=0)
    image =models.ImageField(upload_to='dapp/images')
    pub_date=models.DateField()

    def __str__(self):
        return self.product_name

#Prducts
class Product(models.Model):
    product_id =models.AutoField
    product_name=models.CharField(max_length=120,default="")
    desc=models.CharField(max_length=1020,default="")
    price=models.IntegerField(default=0)
    rating=models.FloatField(default=0)
    image =models.ImageField(upload_to='dapp/images')
    pub_date=models.DateField()

    def __str__(self):
        return self.product_name
#Discounts
class Discount(models.Model):
    discounts_id =models.AutoField
    product_name=models.CharField(max_length=120,default="")
    desc=models.CharField(max_length=1020,default="")
    price=models.IntegerField(default=0)
    orgprice=models.IntegerField(default=0)
    dist=models.IntegerField(default=0)
    rating=models.FloatField(default=0)
    image =models.ImageField(upload_to='dapp/images')
    pub_date=models.DateField()

    def __str__(self):
        return self.product_name
    
class Contact(models.Model):
    msg_id =models.AutoField(primary_key=True)
    name=models.CharField(max_length=120,default="")
    email=models.EmailField(default="")
    _subject=models.CharField(max_length=100,default="")
    message=models.CharField(max_length=620,default="")
    def __str__(self):
        return self.name


    
