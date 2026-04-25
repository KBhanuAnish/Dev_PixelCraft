from django.shortcuts import render
from django.http import HttpResponse
from .models import Vendor
from .forms import VendorProfileEditForm
from Accounts.decorators import ordinary_user_required
from django.contrib.auth.decorators import login_required
from .forms import InventoryItemForm, AddComponentFullForm
# Create your views here.
def Home_page(req):
    return render(req,'Vendors/Home.html',{})
def Dashboard(req):
    return HttpResponse("Dashboard")
def Vendor_profile_edit(req):
    if req.method=='POST':
        model=VendorProfileEditForm(req.POST,req.FILES,instance=req.user.vendor)
        if model.is_valid():
            model.save()
    else:
        model=VendorProfileEditForm(instance=req.user.vendor)
    return render(req,'Vendors/Vendor_Profile_Edit.html',{'form':model})
def Profile(req):
    return render(req,'Vendors/Vendor_Profile.html',{'vendor':req.user.vendor})
@login_required
def Vendors_Inventory(request):
    vendor_items = request.user.vendor.inventory.all().order_by('-created_at')
    return render(request, 'Vendors/Vendor_Inventory.html', {'inventory': vendor_items})


""""Gemini"""
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Components, InventoryItem
from .forms import AddComponentFullForm
# Ensure you import your vendor_required decorator here!

def add_product(request):
    if request.method == 'POST':
        # request.FILES handles the image upload
        form = AddComponentFullForm(request.POST, request.FILES)
        
        if form.is_valid():
            # 1. Look up the component, or create it if it's brand new
            component, created = Components.objects.get_or_create(
                name=form.cleaned_data['name'],
                brand=form.cleaned_data['brand'],
                defaults={
                    'category': form.cleaned_data['category'],
                    'image': form.cleaned_data.get('image'),
                    'description': form.cleaned_data['description'],
                }
            )

            # 2. Check if the vendor is already selling this specific component
            if InventoryItem.objects.filter(vendor=request.user.vendor, component=component).exists():
                messages.error(request, f"You are already selling {component.name}. Update it in your inventory instead.")
                return redirect('vendor_inventory')

            # 3. Add to Vendor Inventory
            InventoryItem.objects.create(
                vendor=request.user.vendor,
                component=component,
                price=form.cleaned_data['price'],
                stock_quantity=form.cleaned_data['stock_quantity']
            )

            if created:
                messages.success(request, f"New component '{component.name}' added to catalog and your shop!")
            else:
                messages.success(request, f"Linked existing component '{component.name}' to your shop!")

            return redirect('vendor_inventory')
    else:
        form = AddComponentFullForm()
    
    return render(request, 'Vendors/vendor_add_component.html', {'form': form})

from django.shortcuts import get_object_or_404
from .models import InventoryItem
from .forms import InventoryItemForm # You can reuse the simple form we made earlier


def edit_inventory_item(request, item_id):
    # Ensure the item exists AND belongs to this vendor
    item = get_object_or_404(InventoryItem, id=item_id, vendor=request.user.vendor)
    
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Updated {item.component.name} successfully!")
            return redirect('vendor_inventory')
    else:
        form = InventoryItemForm(instance=item)
        
    return render(request, 'Vendors/edit_inventory_item.html', {'form': form, 'item': item})


def delete_inventory_item(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id, vendor=request.user.vendor)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item removed from your inventory.")
        return redirect('vendor_inventory')
    return render(request, 'Vendors/confirm_delete.html', {'item': item})