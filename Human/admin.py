from django.contrib import admin

# Register your models here.
from Human.models import Categories, Product, Images

class ProductImageInline(admin.TabularInline):
    model = Images
    extra = 5

class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','image','image_tag']
    list_filter = ['status']
    readonly_fields = ('image_tag',)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'status','category', 'description']
    readonly_fields = ('image_tag',)
    list_filter = ['status']
    inlines = [ProductImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'image_tag']
    readonly_fields = ('image_tag',)


admin.site.register(Categories,CategoriesAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images,ImagesAdmin)