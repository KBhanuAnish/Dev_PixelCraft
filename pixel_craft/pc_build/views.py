from django.shortcuts import render, get_object_or_404
from .models import Components
from Vendors.models import InventoryItem 

def components_list(request):
    components = Components.objects.all()
    return render(request, 'pc_build/components_list.html', {'components': components})

def component_detail(request, pk):
    component = get_object_or_404(Components, pk=pk)
    
    vendor_offers = InventoryItem.objects.filter(
        component=component,
        is_active=True,
        stock_quantity__gt=0
    ).order_by('price')
    
    return render(request, 'pc_build/component_detail.html', {
        'component': component,
        'vendor_offers': vendor_offers
    })