from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _


from .models import (User,)
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'is_active')
    search_fields = ('phone', 'email',)
    list_editable = ('is_active',)
    list_per_page = 10

    def get_fieldsets(self, request, obj=None):
        fieldsets = [None] * 3
        if obj:
            fieldsets[0] = (_('User informations'),
                            {
                'fields': ('email', 'name', 'phone',
                           'user_type')
            })
            fieldsets[1] = (_('Permissions'), {
                'fields': ('verified', 'is_staff', 'is_superuser', ),
            })
            fieldsets[2] = (_('Important dates'), {
                'fields': ('date_joined', 'last_login'),
            })
        else:
            fieldsets[0] = (_('User data'),
                            {
                'fields': ('email', 'phone',
                           'password', 'user_type')
            })
            del fieldsets[1:3]
        return fieldsets

    def get_readonly_fields(self, request, obj=None):
        if obj and request.user.id != obj.id:
            return self.readonly_fields + (
                'email', 'phone', 'date_joined',
                'last_login'
            )
        return self.readonly_fields + ('date_joined', 'last_login')

    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)

admin.site.index_title = _('Special offer admin panel')
admin.site.site_header = _('Special offer Administration')
admin.site.site_title = _('Special offer Management')
