from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    shop_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)

    phone = models.CharField(max_length=15)
    email = models.EmailField()

    address = models.TextField()
    city = models.CharField(max_length=100)

    profile_image = models.ImageField(upload_to='vendors/', blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.shop_name
from django.db import models

class VendorComponent(models.Model):
    vendor = models.ForeignKey(
        'Vendor',
        on_delete=models.CASCADE,
        related_name='vendor_products'
    )
    component = models.ForeignKey(
        'pc_build.Components',
        on_delete=models.CASCADE,
        related_name='component_vendors'
    )

    price = models.FloatField()
    stock = models.PositiveIntegerField()

    is_available = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('vendor', 'component')  # prevent duplicates

    def __str__(self):
        return f"{self.vendor.shop_name} - {self.component.name}"