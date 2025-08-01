from django.contrib import admin
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
    list_display = ('name', 'category', 'base_price', 'in_stock', 'created_at', 'updated_at')
    list_filter = ('category', 'in_stock', 'created_at')
    search_fields = ('name', 'description', 'category__name')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImageInline, ProductVariantInline]
    actions = [mark_in_stock, mark_out_of_stock]

    fieldsets = (
        ("Basic Info", {
            'fields': ('name', 'slug', 'category', 'description', 'has_variants')
        }),
        ("Pricing & Availability", {
            'fields': ('base_price', 'discount_price', 'in_stock')
        }),
        ("Timestamps", {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )


# Register other models as-is
admin.site.register(Category)
admin.site.register(ProductImage)
admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ProductVariant)
admin.site.register(ProductAttribute)
