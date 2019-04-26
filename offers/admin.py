from django.contrib import admin

from galleries.models import (OfferImage, PlusItemImage, DiscountImage)

from .models import (Offer, Category, Discount, PlusItem,
                     BendingOffer, BendingDiscount)
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
                    'price', 'bending',)
    # readonly_fields = ('visited',)
    search_fields = ('id', 'publisher',
                     'publisher__phone', 'category__name', )
    list_filter = ('publisher__name', 'category__name', 'bending',)
    list_editable = ('bending', )
    autocomplete_fields = ('publisher',)
    list_per_page = 10

    def get_exclude(self, request, obj=None):
        if not obj:
            return ['visited', 'likes_count']
        return []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('visited', 'likes_count')
        return self.readonly_fields


class BendingOfferAdmin(admin.ModelAdmin):
    inlines = [
        PlusItemInline,
        OfferImageInline,
    ]
    # raw_id_fields = ('publisher', 'category')
    list_display = ('publisher', 'category', 'name',
                    'price',)
    # readonly_fields = ('visited',)
    search_fields = ('id', 'publisher',
                     'publisher__user__phone', 'category__name', )
    list_filter = ('publisher__name', 'category__name',)
    autocomplete_fields = ('publisher',)
    list_per_page = 10

    def get_exclude(self, request, obj=None):
        if not obj:
            return ['visited', 'likes_count']
        return []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('visited', 'likes_count')
        return self.readonly_fields


class DiscountAdmin(admin.ModelAdmin):
    inlines = [
        DiscountImageInline,
    ]
    # raw_id_fields = ('publisher', 'category')
    list_display = ('publisher', 'category', 'name', 'price',
                    'precentage', 'bending',)
    list_editable = ('bending', )

    search_fields = ('id', 'publisher',
                     'publisher__user__phone', 'category__name',)
    list_filter = ('publisher__name', 'category__name', 'bending',)
    autocomplete_fields = ('publisher',)
    list_per_page = 10

    def get_exclude(self, request, obj=None):
        if not obj:
            return ['visited', 'likes_count']
        return []

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('visited', 'likes_count')
        return self.readonly_fields


class BendingDiscountAdmin(admin.ModelAdmin):
    inlines = [
        DiscountImageInline,
    ]
    # raw_id_fields = ('publisher', 'category')
    list_display = ('publisher', 'category', 'name', 'price',
                    'precentage')

    search_fields = ('id', 'publisher',
                     'publisher__user__phone', 'category__name',)
    list_filter = ('publisher__name', 'category__name')
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
admin.site.register(BendingOffer, BendingOfferAdmin)
admin.site.register(Category)
# admin.site.register(Like)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(BendingDiscount, DiscountAdmin)

# admin.site.register(PlusItem, PlusItemAdmin)
