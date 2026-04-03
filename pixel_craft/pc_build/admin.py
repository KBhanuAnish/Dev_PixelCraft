from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Component

# Optional: display useful fields in the admin list view
@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'brand', 'model', 'release_date')
    search_fields = ('name', 'brand', 'model', 'category')
    list_filter = ('category', 'brand')