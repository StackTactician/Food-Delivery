from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Restaurant, MenuItem, Order, OrderItem
from .forms import UserRegistrationForm, MenuItemForm, UserProfileForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'delivery/register.html', {'form': form})

@login_required
def profile(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'delivery/profile.html', {'form': form})

@login_required
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'delivery/restaurant_list.html', {'restaurants': restaurants})

@login_required
def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    menu_items = restaurant.menu_items.all()
    return render(request, 'delivery/restaurant_detail.html', {'restaurant': restaurant, 'menu_items': menu_items})

@require_POST
def add_to_cart(request, item_id):
    # Check if item exists
    get_object_or_404(MenuItem, pk=item_id)
    # Simple session-based cart
    cart = request.session.get('cart', {})
    cart[str(item_id)] = cart.get(str(item_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total_price = 0
    for item_id, quantity in cart.items():
        menu_item = MenuItem.objects.filter(id=item_id).first()
        if menu_item:
            total_price += menu_item.price * quantity
            items.append({
                'menu_item': menu_item,
                'quantity': quantity,
                'subtotal': menu_item.price * quantity
            })
    
    return render(request, 'delivery/cart.html', {'items': items, 'total_price': total_price})

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('restaurant_list')
    
    if request.method == 'POST':
        # Create Order
        order = Order.objects.create(user=request.user, total_price=0)
        total_price = 0
        
        for item_id, quantity in cart.items():
            menu_item = MenuItem.objects.filter(id=item_id).first()
            if menu_item:
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price_at_time=menu_item.price
                )
                total_price += menu_item.price * quantity
        
        order.total_price = total_price
        order.save()
        
        # Clear cart
        request.session['cart'] = {}
        
        return redirect('order_confirmation', pk=order.pk)
    
    return render(request, 'delivery/checkout.html')

def order_confirmation(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'delivery/order_confirmation.html', {'order': order})

@login_required
def driver_dashboard(request):
    if request.user.userprofile.role != 'Driver':
        return redirect('restaurant_list')
    
    # Handle Availability Toggle
    if request.method == 'POST' and 'toggle_availability' in request.POST:
        profile = request.user.userprofile
        profile.is_available = not profile.is_available
        profile.save()
        return redirect('driver_dashboard')
    
    available_orders = Order.objects.filter(status='Pending', driver=None)
    my_deliveries = Order.objects.filter(driver=request.user).exclude(status='Delivered')
    
    # Calculate Stats
    completed_orders = Order.objects.filter(driver=request.user, status='Delivered')
    completed_jobs_count = completed_orders.count()
    total_earnings = sum(order.total_price for order in completed_orders)
    
    return render(request, 'delivery/driver_dashboard.html', {
        'available_orders': available_orders,
        'my_deliveries': my_deliveries,
        'completed_jobs_count': completed_jobs_count,
        'total_earnings': total_earnings
    })

@login_required
@require_POST
def accept_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.user.userprofile.role == 'Driver' and order.status == 'Pending':
        order.driver = request.user
        order.status = 'Delivering'
        order.save()
    return redirect('driver_dashboard')

@login_required
@require_POST
def complete_order(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.user.userprofile.role == 'Driver' and order.driver == request.user:
        order.driver_confirmed = True
        order.save()
        check_delivery_status(order)
    return redirect('driver_dashboard')

@login_required
def customer_dashboard(request):
    # Active orders: Pending or Delivering
    active_orders = Order.objects.filter(
        user=request.user, 
        status__in=['Pending', 'Delivering']
    ).order_by('-created_at')
    
    # Past orders: Delivered
    past_orders = Order.objects.filter(
        user=request.user, 
        status='Delivered'
    ).order_by('-created_at')[:5] # Get last 5
    
    return render(request, 'delivery/customer_dashboard.html', {
        'active_orders': active_orders,
        'past_orders': past_orders
    })

@login_required
@require_POST
def confirm_delivery_customer(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.user == request.user:
        order.customer_confirmed = True
        order.save()
        check_delivery_status(order)
    return redirect('customer_orders')

def check_delivery_status(order):
    if order.driver_confirmed and order.customer_confirmed:
        order.status = 'Delivered'
        order.save()

@login_required
def manage_restaurants(request):
    if request.user.userprofile.role != 'Restaurant Owner':
        return redirect('restaurant_list')
    
    restaurants = Restaurant.objects.filter(owner=request.user)
    return render(request, 'delivery/manage_restaurants.html', {'restaurants': restaurants})

@login_required
def add_menu_item(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if restaurant.owner != request.user:
        return redirect('restaurant_list')
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant
            menu_item.save()
            return redirect('manage_restaurants')
    else:
        form = MenuItemForm()
    
    return render(request, 'delivery/menu_item_form.html', {'form': form, 'restaurant': restaurant, 'title': 'Add Menu Item'})

@login_required
def edit_menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if menu_item.restaurant.owner != request.user:
        return redirect('restaurant_list')
    
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=menu_item)
        if form.is_valid():
            form.save()
            return redirect('manage_restaurants')
    else:
        form = MenuItemForm(instance=menu_item)
    
    return render(request, 'delivery/menu_item_form.html', {'form': form, 'restaurant': menu_item.restaurant, 'title': 'Edit Menu Item'})

@login_required
def delete_menu_item(request, pk):
    menu_item = get_object_or_404(MenuItem, pk=pk)
    if menu_item.restaurant.owner != request.user:
        return redirect('restaurant_list')
    
    if request.method == 'POST':
        menu_item.delete()
        return redirect('manage_restaurants')
    
    return render(request, 'delivery/menu_item_confirm_delete.html', {'menu_item': menu_item})
