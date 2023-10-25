from django.contrib import admin

from blog.models import Post


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'creation_date')
    list_filter = ('is_published',)
    search_fields = ('title', 'content',)
