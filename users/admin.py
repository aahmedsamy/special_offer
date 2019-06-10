from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from offers.models import (FollowedCategory)
from .models import (User, Searcher, Publisher)
# Register your models here.


class FollowedCategoryInline(admin.TabularInline):
    model = FollowedCategory
    extra = 0


class UserAdmin(admin.ModelAdmin):

    list_display = ('email', 'user_type',
                    'is_active', 'total_visits', )
    search_fields = ('email',)
    list_editable = ('is_active', 'user_type')
    list_per_page = 10

    def get_fieldsets(self, request, obj=None):
        fieldsets = [None] * 3
        if obj:
            fieldsets[0] = (_('User informations'),
                            {
                'fields': ('email', 'name',
                           'user_type')
            })
            fieldsets[1] = (_('Permissions'), {
                'fields': ('verified', ),
            })
            fieldsets[2] = (_('Important dates'), {
                'fields': ('date_joined', 'last_login'),
            })
            fieldsets.append((_('Insights'), {
                'fields': ('total_visits', 'likes_count', 'followers_count'),
            }))
        else:
            fieldsets[0] = (_('User data'),
                            {
                'fields': ('email',
                           'password', 'user_type')
            })
            del fieldsets[1:3]
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj and request.user.id != obj.id:
            return self.readonly_fields + (
                'email', 'date_joined',
                'last_login', 'total_visits', 'likes_count', 'followers_count'
            )
        return self.readonly_fields + ('date_joined', 'last_login',
                                       'total_visits', 'likes_count', 'followers_count')

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


class PublisherInline(admin.StackedInline):
    model = User

    def get_fieldsets(self, request, obj=None):
        fieldsets = [None] * 3

        fieldsets[0] = (_('User informations'),
                        {
            'fields': ('email',
                       )
        })
        fieldsets[1] = (_('Permissions'), {
            'fields': ('verified', ),
        })
        fieldsets[2] = (_('Important dates'), {
            'fields': ('date_joined', 'last_login'),
        })
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('email', 'verified',
                                       'date_joined', 'last_login')


class SearcherInline(admin.StackedInline):
    model = User

    def get_fieldsets(self, request, obj=None):
        fieldsets = [None] * 2

        fieldsets[0] = (_('User informations'),
                        {
            'fields': ('email',
                       )
        })
        fieldsets[1] = (_('Important dates'), {
            'fields': ('date_joined', 'last_login'),
        })
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields + ('email', 'verified',
                                       'date_joined', 'last_login')


class SearcherAdmin(admin.ModelAdmin):
    inlines = [
        FollowedCategoryInline,
    ]
    list_display = ('name', 'email',)

    def get_fieldsets(self, request, obj=None):
        fieldsets = [None] * 3

        fieldsets[0] = (_('User informations'),
                        {
            'fields': ('name', 'email')
        })
        fieldsets[1] = (_('Insights'), {
            'fields': ('following_count',),
        })
        fieldsets[2] = (_('Important dates'), {
            'fields': ('date_joined', 'last_login'),
        })
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('name', 'email', 'date_joined',
                                           'following_count', 'last_login', 'verified')
        return self.readonly_fields

    def has_add_permission(self, request):
        return False


class PublisherAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name',)
    list_display = ('name', 'email', 'verified')

    def get_fieldsets(self, request, obj=None):
        fieldsets = [None] * 5

        fieldsets[0] = (_('User informations'),
                        {
            'fields': ('name', 'phone', 'email', 'image', 'trading_doc')
        })
        fieldsets[1] = (_('Links'), {
            'fields': ('address_url', 'website_url', 'facebook_url',
                       'twitter_url', 'instgram_url'),
        })
        fieldsets[2] = (_('Permissions'), {
            'fields': ('verified', ),
        })
        fieldsets[3] = (_('Important dates'), {
            'fields': ('date_joined', 'last_login'),
        })
        fieldsets[4] = (_('Insights'), {
            'fields': ('total_visits', 'likes'),
        })
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('name', 'image', 'address_url',
                                           'website_url', 'facebook_url',
                                           'twitter_url', 'instgram_url',
                                           'trading_doc', 'work_start_at',
                                           'work_end_at', 'total_visits',
                                           'likes', 'last_login', 'date_joined',
                                           'verified', 'phone', 'email',
                                           'followers_count')
        return self.readonly_fields

    def has_add_permission(self, request):
        return False


admin.site.unregister(Group)

admin.site.register(Searcher, SearcherAdmin)
admin.site.register(Publisher, PublisherAdmin)

admin.site.index_title = _('Special offer admin panel')
admin.site.site_header = _('Special offer Administration')
admin.site.site_title = _('Special offer Management')
