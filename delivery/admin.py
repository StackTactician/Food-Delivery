from django.contrib import admin
from .models import Restaurant, MenuItem, Order, OrderItem, UserProfile

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

class RestaurantAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('price_at_time',)

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(MenuItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(UserProfile)
