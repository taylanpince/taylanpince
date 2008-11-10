from django.contrib import admin

from applications.models import TenantApplication


class TenantApplicationAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "phone", "email", "application_date", "reviewed")
    list_display_links = ("first_name", "last_name")
    list_filter = ("reviewed",)


admin.site.register(TenantApplication, TenantApplicationAdmin)
