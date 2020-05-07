from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactFormMessage, UserProfile


class ContactFormMessageAdmin(admin.ModelAdmin): # ContactFromMessageAdmin modeli olarak ne gösterilsin ?
    list_display = ['name','email','subject','note','status']  # sıralı olarak ne ler gösterilsin ?
    list_filter = ['status'] # Status e göre filtreleme yapılsın.


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','phone','city','country','image_tag',]


admin.site.register(ContactFormMessage,ContactFormMessageAdmin) # Contact
admin.site.register(Setting) # admin sitesinde göster.
admin.site.register(UserProfile,UserProfileAdmin) # Contact
