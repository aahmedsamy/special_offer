from django.contrib import admin

from galleries.models import (OfferImage, PlusItemImage, DiscountImage)

from .models import (Offer, Category, Discount, PlusItem)
# Register your models here.


class OfferImageInline(admin.TabularInline):
    model = OfferImage
    exclude = ('small_image_path', )
    extra = 2


class PlusItemImageInline(admin.TabularInline):
    model = PlusItemImage
    exclude = ('small_image_path', )
    extra = 2


class DiscountImageInline(admin.TabularInline):
    model = DiscountImage
    exclude = ('small_image_path', )
    extra = 2


class PlusItemInline(admin.TabularInline):
    model = PlusItem
    extra = 2


class OfferAdmin(admin.ModelAdmin):
    inlines = [
        PlusItemInline,
        OfferImageInline,
    ]
    # raw_id_fields = ('publisher', 'category')
    list_display = ('publisher', 'category', 'name',
                    'price', 'visible', 'bending',)
    # readonly_fields = ('visited',)
    search_fields = ('id', 'publisher',
                     'publisher__phone', 'category__name', )
    list_filter = ('publisher__name', 'category__name', 'bending', 'visible')
    list_editable = ('visible', 'bending', )
    autocomplete_fields = ('publisher',)
    list_per_page = 10

    def get_exclude(self, request, obj=None):
        if not obj:
            return ['visited']
        return []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('visited',)
        return self.readonly_fields


class DiscountAdmin(admin.ModelAdmin):
    inlines = [
        DiscountImageInline,
    ]
    # raw_id_fields = ('publisher', 'category')
    list_display = ('publisher', 'category', 'name', 'price',
                    'precentage', 'bending', 'visible')
    list_editable = ('visible', 'bending', )

    search_fields = ('id', 'publisher',
                     'publisher__phone', 'category__name',)
    list_filter = ('publisher__name', 'category__name', 'bending', 'visible')
    autocomplete_fields = ('publisher',)
    list_per_page = 10

    def get_exclude(self, request, obj=None):
        if not obj:
            return ['visited']
        return []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('visited',)
        return self.readonly_fields


# class PlusItemAdmin(admin.ModelAdmin):
#     inlines = [
#         PlusItemImageInline,
#     ]
#     raw_id_fields = ('offer',)
#     list_display = ('offer', 'name',)

#     search_fields = ('name',)
#     # autocomplete_fields = ('publisher',)
#     list_per_page = 10


admin.site.register(Offer, OfferAdmin)
admin.site.register(Category)
admin.site.register(Discount, DiscountAdmin)
# admin.site.register(PlusItem, PlusItemAdmin)
