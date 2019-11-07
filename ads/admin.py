from django.contrib import admin
from .models import Ad
# Register your models here.


class AdAdmin(admin.ModelAdmin):
    list_display = ('advertiser', 'name', 'start_date',
                    'end_date', 'period', 'position')
    list_editable = ('position',)
    # search_fields = ('advertiser_id', 'advertiser', 'offer_id', 'discount_id')
    search_fields = ('advertiser_id', 'advertiser')
    # autocomplete_fields = ('advertiser', 'offer', 'discount')
    autocomplete_fields = ('advertiser',)


admin.site.register(Ad, AdAdmin)
