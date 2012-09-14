from django.contrib import admin
from myblog.insta_blog import models

class ArticleAdmin(admin.ModelAdmin):
	list_display = ('title','time_posted','author','status')
	list_filter = ('time_posted',)
	search_fields = ('title','author')
	date_hierarchy='time_posted'
	ordering = ('-time_posted','status')
	prepopulated_fields = {"slug": ("title",)}


admin.site.register(models.Article,ArticleAdmin)

