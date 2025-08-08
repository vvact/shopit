from django.contrib import admin
from .models import Category, FlashDeal
from .models import (
    Category,
    Product,
    ProductImage,
    Attribute,
    AttributeValue,
    Color,
    Size,
    ProductVariant,
    ProductAttribute,
)

from django.contrib.sessions.models import Session

# Product Image Inline
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'position', 'is_main']
    ordering = ['position']

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if instance.is_main:
                # Unset other main images for this product
                ProductImage.objects.filter(product=instance.product).exclude(id=instance.id).update(is_main=False)
            instance.save()
        formset.save_m2m()


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('color', 'size', 'image', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    show_change_link = True


# Actions
@admin.action(description="Mark selected products as in stock")
def mark_in_stock(modeladmin, request, queryset):
    queryset.update(in_stock=True)

@admin.action(description="Mark selected products as out of stock")
def mark_out_of_stock(modeladmin, request, queryset):
    queryset.update(in_stock=False)


# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'in_stock', 'is_featured', 'created_at', 'updated_at')
    list_filter = ('category', 'in_stock', 'is_featured', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImageInline, ProductVariantInline]
    actions = [mark_in_stock, mark_out_of_stock]

    fieldsets = (
        ("Basic Info", {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ("Pricing & Availability", {
            'fields': ('base_price', 'discount_price', 'in_stock', 'is_featured')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )



class ProductInline(admin.TabularInline):
    model = FlashDeal
    extra = 1

@admin.register(FlashDeal)
class FlashDealAdmin(admin.ModelAdmin):
    list_display = ('title', 'product', 'start_time', 'end_time', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title',)




# products/admin.py

# admin.py

from django.contrib import admin
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['indented_name', 'slug', 'parent', 'level']
    list_filter = ['parent']
    search_fields = ['name', 'slug']

    def indented_name(self, obj):
        return '— ' * obj.level + obj.name
    indented_name.short_description = 'Category'

    def level(self, obj):
        return obj.level


admin.site.register(ProductImage)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ProductVariant)
admin.site.register(ProductAttribute)
admin.site.register(Session)
