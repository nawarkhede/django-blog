from django.contrib import admin

# Register your models here.

from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "publish", "status", "blog_post"]
    list_filter = ["status", "created", "publish", "author"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ["author"]
    date_hierarchy = "publish"
    ordering = ["status", "publish"]


class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "body", "post", "created_on", "active"]
    search_fields = ["name", "email", "body"]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
