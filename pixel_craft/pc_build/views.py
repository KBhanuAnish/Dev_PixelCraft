from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Imports from your pc_build models
from .models import CartItem, CustomBuild, Order, OrderItem

# Imports from your Vendors models
from Vendors.models import InventoryItem, Components

# ---------------------------------------------------------
# CATALOG VIEWS
# ---------------------------------------------------------

def components_list(request):
    """Shows all hardware in the catalog."""
    components = Components.objects.all()
    return render(request, 'pc_build/components_list.html', {'components': components})

def component_detail(request, pk):
    """Shows details for a specific component and all vendors selling it."""
    component = get_object_or_404(Components, pk=pk)
    
    # Fetch all active vendor offers for this specific part, cheapest first
    vendor_offers = InventoryItem.objects.filter(
        component=component,
        is_active=True,
        stock_quantity__gt=0
    ).order_by('price')
    
    return render(request, 'pc_build/component_detail.html', {
        'component': component,
        'vendor_offers': vendor_offers
    })

# ---------------------------------------------------------
# CART VIEWS
# ---------------------------------------------------------

@login_required
def add_to_cart(request, inventory_id):
    """Adds a single vendor component to the cart."""
    inventory_item = get_object_or_404(InventoryItem, id=inventory_id)
    
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        inventory_item=inventory_item,
        custom_build=None 
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Updated quantity of {inventory_item.component.name} in your cart.")
    else:
        messages.success(request, f"Added {inventory_item.component.name} to your cart.")
        
    return redirect('cart_view')

@login_required
def remove_from_cart(request, cart_item_id):
    """Removes an item or build from the cart."""
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.warning(request, "Item removed from cart.")
    return redirect('cart_view')

@login_required
def cart_view(request):
    """Displays the user's shopping cart."""
    cart_items = CartItem.objects.filter(user=request.user).order_by('-added_at')
    cart_total = sum(item.item_total for item in cart_items)
    
    return render(request, 'pc_build/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

# ---------------------------------------------------------
# CHECKOUT & ORDER VIEWS
# ---------------------------------------------------------

@login_required
def checkout_view(request):
    """Handles checkout and explodes hybrid builds into individual vendor orders."""
    cart_items = CartItem.objects.filter(user=request.user)
    
    if not cart_items.exists():
        messages.error(request, "Your cart is empty.")
        return redirect('cart_view')

    if request.method == 'POST':
        cart_total = sum(item.item_total for item in cart_items)
        
        # 1. Create the Main Order
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name', request.user.username),
            shipping_address=request.POST.get('shipping_address', 'Address provided at checkout'),
            total_amount=cart_total
        )
        
        # 2. Loop through Cart and "Flatten" into OrderItems
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
        
        # 3. Empty the Cart
        cart_items.delete()
        messages.success(request, f"Order #{order.id} placed successfully! Vendors have been notified.")
        return redirect('order_history')

    return render(request, 'pc_build/checkout.html', {'cart_items': cart_items})

@login_required
def order_history(request):
    """Customer View: Shows all orders placed by this user."""
    orders = Order.objects.filter(user=request.user).order_by('-created_at').prefetch_related('items__inventory_item__component')
    return render(request, 'pc_build/order_history.html', {'orders': orders})
# Make sure get_object_or_404 is imported at the top of your file!

@login_required
def mark_as_delivered(request, item_id):
    """Allows the customer to confirm they received a specific shipped item."""
    if request.method == 'POST':
        # Find the specific item, but ONLY if it belongs to an order owned by this user
        item = get_object_or_404(OrderItem, id=item_id, order__user=request.user)
        
        # Only update it if it's currently marked as Shipped
        if item.vendor_status == 'Shipped':
            item.vendor_status = 'Delivered'
            item.save()
            messages.success(request, f"Awesome! {item.inventory_item.component.name} marked as Delivered.")
            
            # SMART LOGIC: Check if the entire Master Order is fully delivered now
            main_order = item.order
            # If there are NO items left in this order that aren't "Delivered"...
            if not main_order.items.exclude(vendor_status='Delivered').exists():
                main_order.status = 'Completed'
                main_order.save()
                messages.success(request, f"Order #{main_order.id} is now fully completed!")
                
    return redirect('order_history')
