from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from batchadmin.admin import BatchModelAdmin

from blog.models import Category, PostType, Post, Comment


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


class CommentAdmin(BatchModelAdmin):
    list_display = ("post", "author", "email", "body", "creation_date", "change_date", "published")
    list_filter = ["published"]
    
    search_fields = ("author", "email", "body", "url")
    
    save_on_top = True
    
    fieldsets = (
        (_("Content"), {
            "fields": ("body",),
        }),
        (_("Author"), {
            "fields": ("author", "email", "url", "ip_address"),
        }),
        (_("Relations"), {
            "fields": ("post",),
        }),
        (_("Publication Settings"), {
            "fields": ("published", "creation_date"),
            "classes": ["collapse"],
        }),
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(PostType, PostTypeAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
