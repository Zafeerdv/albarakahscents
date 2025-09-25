from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from .models import Category, Product, ProductImage
from .models import Order, OrderItem

class UserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'full_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, UserAdmin)

# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # default 1 empty form
    fields = ('image', 'alt_text', 'position')
    readonly_fields = ()
    ordering = ('position',)

# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'original_price', 'discount_price', 'size', 'stock')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('product', 'quantity', 'price')
    extra = 0
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]