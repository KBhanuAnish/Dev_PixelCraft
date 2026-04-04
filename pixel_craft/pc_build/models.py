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

    price = models.DecimalField(max_digits=10, decimal_places=2)

    stock = models.PositiveIntegerField(default=0)

    image_url = models.URLField(max_length=500, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    specs=models.TextField(blank=True, null=True)

    rating = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name