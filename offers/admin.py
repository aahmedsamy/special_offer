from django.contrib import admin

from galleries.models import (OfferImage, PlusItemImage, DiscountImage)

from .models import (Offer, Category, Discount, PlusItem)
# Register your models here.


class OfferImageInline(admin.TabularInline):
    model = OfferImage
    exclude = ('small_image_path', )
    extra = 1


class PlusItemImageInline(admin.TabularInline):
    model = PlusItemImage
    exclude = ('small_image_path', )
    extra = 1


class DiscountImageInline(admin.TabularInline):
    model = DiscountImage
    exclude = ('small_image_path', )
    extra = 1


class PlusItemInline(admin.TabularInline):
    model = PlusItem
    extra = 1


class OfferAdmin(admin.ModelAdmin):
    inlines = [
        OfferImageInline,
        PlusItemInline
    ]
    raw_id_fields = ('publisher', 'category')
    list_display = ('publisher', 'category', 'name', 'price')
    readonly_fields = ('visited',)
    search_fields = ('id', 'publisher',
                     'publisher__phone', 'category__name')
    list_filter = ('publisher__name', 'category__name')
    # autocomplete_fields = ('publisher',)
    list_per_page = 10


class DiscountAdmin(admin.ModelAdmin):
    inlines = [
        DiscountImageInline,
    ]
    raw_id_fields = ('publisher', 'category')
    list_display = ('publisher', 'category', 'name', 'price', 'precentage')
    readonly_fields = ('visited',)
    search_fields = ('id', 'publisher',
                     'publisher__phone', 'category__name')
    list_filter = ('publisher__name', 'category__name')
    # autocomplete_fields = ('publisher',)
    list_per_page = 10


class PlusItemAdmin(admin.ModelAdmin):
    inlines = [
        PlusItemImageInline,
    ]
    raw_id_fields = ('offer',)
    list_display = ('offer', 'name', )
    search_fields = ('name',)
    # autocomplete_fields = ('publisher',)
    list_per_page = 10


admin.site.register(Offer, OfferAdmin)
admin.site.register(Category)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(PlusItem, PlusItemAdmin)
