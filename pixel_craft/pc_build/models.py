from django.db import models

class Component(models.Model):
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
        # Add more categories if needed
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    technical_specs = models.JSONField(default=dict, help_text="e.g., {'socket': 'AM4', 'ram_type': 'DDR4'}")
    
    # Store image directly in DB
    image_data = models.BinaryField(blank=True, null=True, help_text="Raw image bytes")
    image_mime = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., image/png or image/jpeg")
    
    release_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.category})"