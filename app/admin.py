from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NewUser, Product, Influencerinfo, Customer, Cart, OrderPlaced, InfluencerCart, Return, Size, Color
# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import admin


'''class CustomUserAdmin(UserAdmin):
    fieldsets = (

        *UserAdmin.fieldsets,
        (
            'Additional Info',
            {
                'fields':(
                    'user_phonenumber',
                    'influencercode'
                )
            }
        )
    )

admin.site.register(NewUser, CustomUserAdmin)'''

class NewUserAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'user_phonenumber', 'influencercode', 'influencerinstagram')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ( 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


admin.site.register(get_user_model(), NewUserAdmin)

# fields = list(UserAdmin.fieldsets)
# fields[1] = ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'user_phonenumber', 'influencercode', 'influencerinstagram')})
# UserAdmin.fieldsets = tuple(fields)

# admin.site.register(NewUser, UserAdmin)

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'selling_price', 'discounted_price', 'description', 'brand', 'category', 'product_image',  'display_sizes', 'display_colors', 'factory', 'commission']

    def display_sizes(self, obj):
        return ", ".join([size.name for size in obj.size.all()])

    def display_colors(self, obj):
        return ", ".join([color.name for color in obj.colors.all()])
    
# admin.site.register(Product, ProductModelAdmin)
admin.site.register(Size)
admin.site.register(Color)


@admin.register(Influencerinfo)
class InfluencerinfoModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'influencer_name', 'influencer_phone', 'influencer_email', 'influencer_code', 'password']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'locality', 'city', 'zipcode', 'state']



@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'quantity', 'color', 'size']

@admin.register(InfluencerCart)
class InfluencerCartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'code']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    def customer_info(self, obj):
     link = reverse("admin:app_customer_change", args=[obj.customer.pk])
     return format_html('<a href="{}">{}</a>', link, obj.customer.name)
    
    customer_info.short_description = 'Customer Info'

    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

    product_info.short_description = 'Product Info'
    list_display = ['id', 'user', 'customer',  'customer_info', 'product', 'product_info', 'quantity', 'ordered_date', 'color', 'size', 'status', 'influencercode']



@admin.register(Return)
class ReturnModelAdmin(admin.ModelAdmin):
    def product_info(self, obj):
        link = reverse("admin:app_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

    product_info.short_description = 'Product Info'
    list_display = ['id', 'user', 'product', 'product_info', 'reason', 'Returned_date']





    