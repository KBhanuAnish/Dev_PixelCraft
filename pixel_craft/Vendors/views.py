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
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vendor
from pc_build.models import OrderItem  # Ensure this imports your OrderItem from the pc_build app!

@login_required
def vendor_orders_view(request):
    try:
        # Get the vendor profile linked to the logged-in user
        my_vendor_profile = request.user.vendor
    except Vendor.DoesNotExist:
        messages.error(request, "You do not have a registered vendor account.")
        return redirect('Vendors_Home')

    # Handle the "Mark as Shipped" button click
    if request.method == 'POST':
        order_item_id = request.POST.get('order_item_id')
        if order_item_id:
            # Find the specific item and ensure it belongs to this vendor
            item_to_update = OrderItem.objects.get(id=order_item_id, vendor=my_vendor_profile)
            item_to_update.vendor_status = 'Shipped'
            item_to_update.save()
            messages.success(request, f"Order #{item_to_update.order.id} marked as Shipped!")
            return redirect('vendor_orders')

    # Fetch Pending Orders (Needs to be shipped)
    pending_orders = OrderItem.objects.filter(
        vendor=my_vendor_profile, 
        vendor_status='Pending'
    ).order_by('-order__created_at')

    # Fetch Shipped/Completed Orders (History)
    shipped_orders = OrderItem.objects.filter(
        vendor=my_vendor_profile, 
        vendor_status__in=['Shipped', 'Delivered']
    ).order_by('-order__created_at')

    return render(request, 'Vendors/vendor_orders.html', {
        'pending_orders': pending_orders,
        'shipped_orders': shipped_orders
    })
# Make sure these imports are at the top of your file!
from .models import Vendor, InventoryItem, Components  # Keeps your Vendor imports safe
from pc_build.models import Order, OrderItem           # Pulls the Orders from the pc_build app!
from Vendors.models import Vendor

# --- Paste this at the bottom of pc_build/views.py ---

@login_required
def checkout_view(request):
    """Handles the checkout process and explodes hybrid builds into individual vendor orders."""
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_view')

    if request.method == 'POST':
        cart_total = sum(item.item_total for item in cart_items)
        
        # Create the Main Order
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name', request.user.username),
            shipping_address=request.POST.get('shipping_address', 'Address provided at checkout'),
            total_amount=cart_total
        )
        
        # Loop through Cart and "Flatten" into OrderItems
        for cart_item in cart_items:
            if cart_item.inventory_item:
                # Single Item
                OrderItem.objects.create(
                    order=order,
                    vendor=cart_item.inventory_item.vendor,
                    inventory_item=cart_item.inventory_item,
                    price_at_purchase=cart_item.inventory_item.price,
                    quantity=cart_item.quantity
                )
                cart_item.inventory_item.stock_quantity -= cart_item.quantity
                cart_item.inventory_item.save()
                
            elif cart_item.custom_build:
                # Hybrid Build
                for build_item in cart_item.custom_build.items.all():
                    OrderItem.objects.create(
                        order=order,
                        vendor=build_item.inventory_item.vendor,
                        inventory_item=build_item.inventory_item,
                        price_at_purchase=build_item.inventory_item.price,
                        quantity=cart_item.quantity
                    )
                    build_item.inventory_item.stock_quantity -= cart_item.quantity
                    build_item.inventory_item.save()
        
        # Empty the Cart
        cart_items.delete()
        messages.success(request, f"Order #{order.id} placed successfully! Vendors have been notified.")
        return redirect('order_history')

    return render(request, 'pc_build/checkout.html', {'cart_items': cart_items})

@login_required
def order_history(request):
    """Customer View: Shows all orders placed by this user."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items__inventory_item__component')
    return render(request, 'pc_build/order_history.html', {'orders': orders})
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from pc_build.models import OrderItem, Order
@login_required
def Dashboard(request):
    vendor = request.user.vendor
    # Focus on things that need ACTION
    pending_items = OrderItem.objects.filter(vendor=vendor, vendor_status='Pending')
    low_stock = vendor.inventory.filter(stock_quantity__lt=5) # Alert if stock is less than 5
    
    return render(request, 'Vendors/dashboard.html', {
        'pending_items': pending_items,
        'low_stock': low_stock,
    })

@login_required
def vendor_analytics(request):
    vendor = request.user.vendor
    # Focus on MONEY and TRENDS
    revenue_data = OrderItem.objects.filter(vendor=vendor, vendor_status='Delivered').aggregate(Sum('price_at_purchase'))
    
    # Logic to find the most popular item
    best_seller = OrderItem.objects.filter(vendor=vendor).values('inventory_item__component__name').annotate(count=Count('id')).order_by('-count').first()

    return render(request, 'Vendors/analytics.html', {
        'total_revenue': revenue_data['price_at_purchase__sum'] or 0,
        'best_seller': best_seller,
    })