from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    category = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255)
    price = models.IntegerField(default=0) 
    cost = models.IntegerField(default=0)
    expiration_date = models.DateField(null=True)
    size = models.CharField(choices=[('small', 'Small'), ('large', 'Large')], max_length=10)
    account = models.ForeignKey('accounts.Account', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-id"]

