from django.contrib import admin

from galleries.models import (OfferImage, PlusItemImage, DiscountImage)

from .models import (Offer, Category, Discount, PlusItem,
                     PendingOffer, PendingDiscount, OfferAndDiscountFeature, Story, PendingStory)
# Register your models here.


class OfferImageInline(admin.TabularInline):
    model = OfferImage
    exclude = ('small_image_path', )
    extra = 2


class FeatureInline(admin.TabularInline):
    model = OfferAndDiscountFeature
    readonly_fields = ("offer", "discount")
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
        FeatureInline
    ]
    # raw_id_fields = ('publisher', 'category')
    list_display = ('publisher', 'category', 'name',
                    'price', 'status',)
    # readonly_fields = ('visited',)
    search_fields = ('id', 'publisher',
                     'publisher__phone', 'category__name', )
    list_filter = ('publisher__name', 'category__name', 'status',)
    list_editable = ('status', )
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


class PendingOfferAdmin(admin.ModelAdmin):
    inlines = [
        PlusItemInline,
        OfferImageInline,
        FeatureInline,
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
        FeatureInline
    ]
    # raw_id_fields = ('publisher', 'category')
    list_display = ('publisher', 'category', 'name',
                    'precentage', 'status',)
    list_editable = ('status', )

    search_fields = ('id', 'publisher',
                     'publisher__user__phone', 'category__name',)
    list_filter = ('publisher__name', 'category__name', 'status',)
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


class PendingDiscountAdmin(admin.ModelAdmin):
    inlines = [
        DiscountImageInline,
    ]
    # raw_id_fields = ('publisher', 'category')
    list_display = ('publisher', 'category', 'name',
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


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name', 'image')
    list_filter = ('name',)
    list_per_page = 10

class StoryAdmin(admin.ModelAdmin):
    # raw_id_fields = ('publisher', 'category')
    list_display = ('advertiser', 'start_time', 'number_of_hours', 'status')
    # readonly_fields = ('visited',)
    search_fields = ('id', 'advertiser',
                     'advertiser__phone', )
    list_filter = ('advertiser__name', 'status',)
    list_editable = ('status', )
    autocomplete_fields = ('advertiser',)
    list_per_page = 10


admin.site.register(Offer, OfferAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(PendingStory, StoryAdmin)
admin.site.register(PendingOffer, PendingOfferAdmin)
admin.site.register(Category, CategoryAdmin)
# admin.site.register(Like)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(PendingDiscount, DiscountAdmin)

# admin.site.register(PlusItem, PlusItemAdmin)
