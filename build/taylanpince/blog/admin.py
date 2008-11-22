from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from blog.models import Category, PostType, Post


class CategoryAdmin(admin.ModelAdmin):
    pass


class PostTypeAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "creation_date", "change_date", "published")
    list_filter = ["published"]
    
    search_fields = ("title", "teaser", "body", "tags")
    
    save_on_top = True
    
    fieldsets = (
        (_("Content"), {
            "fields": ("title", "teaser", "body", "link", "tags"),
        }),
        (_("Relations"), {
            "fields": ("categories", "type"),
        }),
        (_("Publication Settings"), {
            "fields": ("published", "slug", "creation_date"),
            "classes": ["collapse"],
        }),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(PostType, PostTypeAdmin)
admin.site.register(Post, PostAdmin)
