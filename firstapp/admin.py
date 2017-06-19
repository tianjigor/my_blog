import sys
reload(sys)
sys.setdefaultencoding("utf8")
from django.contrib import admin

# Register your models here.
from firstapp.models import Article, Comment, UserProfile, Tickets, Category, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_time', 'modified_time', 'category', ]

admin.site.register(Article, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag)

admin.site.register(Comment)
admin.site.register(UserProfile)
admin.site.register(Tickets)
