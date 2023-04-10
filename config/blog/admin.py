from django.contrib import admin
from .models import Category, Article, ArticleReport, ArticleReturn

# Register your models here.


class ArticleAdmin(admin.ModelAdmin):

    list_display = ['title', 'slug', 'category_to_str', 'jalali_publish_date', 'jalali_creation_date', 'jalali_update_date', 'status']
    list_filter = ('publish_date', 'status')
    search_fields = ('title', 'description')
    # prepopulated_fields = { 'slug' : ('title',) }
    ordering = ['status', 'publish_date']


    def category_to_str(self, obj):
        return "".join([category.title for category in obj.category.all()])
    category_to_str.short_description =  "دسته بندی ها"







class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status', 'level']
    readonly_fields = ['level']
    list_filter = ('status', 'level')
    search_fields = ('title', 'slug')
    # prepopulated_fields = { 'slug' : ('title',) }






# class ArticleHistoryAdmin(admin.ModelAdmin):
#     list_display = ['title', 'article', 'article_after_delete', 'slug', 'category_to_str', 'thumbnail', 'jalali_publish_date', 'jalali_creation_date', 'jalali_update_date', 'status']
#     search_fields = ('title', 'description')
#     ordering = ['status', 'publish_date']

#     def category_to_str(self, obj):
#         category_list = []
#         for category in obj.completed_cateogry():
#             category_list.append(category)
#         return category_list
#     category_to_str.short_description =  "دسته بندی ها"




class ArticleReportAdmin(admin.ModelAdmin):
    list_display = ['article', 'reason', 'description', 'creation_date', 'is_checked']
    list_filter = ('article', 'reason', 'is_checked')
    search_fields = ('article', 'reason')




class ArticleReturnAdmin(admin.ModelAdmin):
    list_display = ['article', 'reason', 'description', 'creation_date', 'is_checked']
    list_filter = ('article', 'reason', 'is_checked')
    search_fields = ('article', 'reason')





admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
# admin.site.register(ArticleHistory, ArticleHistoryAdmin)
admin.site.register(ArticleReport, ArticleReportAdmin)
admin.site.register(ArticleReturn, ArticleReturnAdmin)
