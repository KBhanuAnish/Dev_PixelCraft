from django.db import models

class Components(models.Model):

    CATEGORY_CHOICES = [
        ('CPU', 'CPU'),
        ('GPU', 'GPU'),
        ('RAM', 'RAM'),
        ('Motherboard', 'Motherboard'),
        ('PSU', 'PSU'),
        ('Storage', 'Storage'),
        ('Case', 'Case'),
        ('Cooler', 'Cooler'),
        ('Monitor', 'Monitor'),
        ('Peripheral', 'Peripheral'),
    ]

    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    image = models.ImageField(upload_to='component_images/', blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    specs = models.TextField(blank=True, null=True)

    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
from django.db import models
from django.conf import settings
from Vendors.models import InventoryItem



class CustomBuild(models.Model):
    """The 'Wrapper' for a user's custom PC."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='custom_builds')
    name = models.CharField(max_length=100, default="My Custom PC")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    @property
    def total_build_price(self):
        # Calculates the sum of all parts inside this specific build
        total = sum(item.inventory_item.price for item in self.items.all())
        return total

class CustomBuildItem(models.Model):
    """The specific vendor parts inside the Custom Build."""
    build = models.ForeignKey(CustomBuild, on_delete=models.CASCADE, related_name='items')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.inventory_item.component.name} in {self.build.name}"




class CartItem(models.Model):
    """Holds EITHER a single part OR a whole custom build."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    
    # EITHER this is filled out (Normal Item)...
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, null=True, blank=True)
    
    # ...OR this is filled out (Hybrid Pre-build)
    custom_build = models.ForeignKey(CustomBuild, on_delete=models.CASCADE, null=True, blank=True)
    
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.inventory_item:
            return f"Cart: {self.inventory_item.component.name}"
        if self.custom_build:
            return f"Cart: {self.custom_build.name}"
        return "Cart Item"
    
    @property
    def item_total(self):
        # Math gets super easy here!
        if self.inventory_item:
            return self.inventory_item.price * self.quantity
        elif self.custom_build:
            return self.custom_build.total_build_price * self.quantity
        return 0
    
# Add these underneath your Cart models in pc_build/models.py
from Vendors.models import Vendor # Make sure to import your Vendor model

class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=255)
    shipping_address = models.TextField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    ITEM_STATUS = (
        ('Pending', 'Pending Vendor Approval'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='vendor_orders')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.SET_NULL, null=True)
    
    # We save the price just in case the vendor changes it later!
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    vendor_status = models.CharField(max_length=20, choices=ITEM_STATUS, default='Pending')

    def __str__(self):
        return f"{self.inventory_item.component.name} (Order #{self.order.id})"