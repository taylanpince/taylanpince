from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from portfolio.models import Category, Photo, Piece


class CategoryAdmin(admin.ModelAdmin):
    pass


class PhotoAdmin(admin.StackedInline):
    model = Photo


class PieceAdmin(admin.ModelAdmin):
    list_display = ("title", "creation_date", "published")
    list_filter = ["published"]
    inlines = [
        PhotoAdmin,
    ]
    
    search_fields = ("title", "teaser", "body")
    
    save_on_top = True
    
    fieldsets = (
        (_("Content"), {
            "fields": ("title", "teaser", "body", "link"),
        }),
        (_("Relations"), {
            "fields": ("categories", ),
        }),
        (_("Publication Settings"), {
            "fields": ("published", "slug", "creation_date"),
            "classes": ["collapse"],
        }),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Piece, PieceAdmin)
