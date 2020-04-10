from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField

class Categories(models.Model):
    STATUS = (
        ('True','Evet'),
        ('False','Hayır'),
    )
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    image = models.ImageField(blank=True,upload_to='images/')
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    parent = models.ForeignKey('self',blank=True,null=True,related_name='children',on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Product(models.Model):
    STATUS = (
        ('True','Evet'),
        ('False','Hayır'),
    )
    name= models.CharField(max_length=20)
    email=models.CharField(max_length=50)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE) # bu product kategoriyle ilişki ile kurar
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    image = models.ImageField(blank=True,upload_to='images/'),
    status = models.CharField(max_length=10, choices=STATUS)
    detail = models.TextField()
    #detail = RichTextUploadingField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Images(models.Model):
    photo = models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(blank=True,upload_to='images/')
    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'