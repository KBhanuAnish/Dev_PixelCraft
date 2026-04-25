from django.contrib import admin
from .models import Components

@admin.register(Components)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand',  'created_at')
    search_fields = ('name', 'brand', 'category')
    list_filter = ('category', 'brand')