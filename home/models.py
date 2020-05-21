from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe


class Setting(models.Model) :
    STATUS = (  # seçim yapılması için
        ('True', 'Evet'),
        ('False','Hayır'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True,max_length=150)
    phone = models.CharField(blank=True,max_length=15)
    fax = models.CharField(blank=True,max_length=15)
    email = models.CharField(blank=True,max_length=50)
    smtpserver = models.CharField(blank=True,max_length=20)
    smtpemail = models.CharField(blank=True,max_length=20)
    smtppassword = models.CharField(blank=True,max_length=10)
    smtpport = models.CharField(blank=True,max_length=5)
    icon = models.ImageField(blank=True,upload_to='images/') # imageler nereye yüklensin ?
    facebook = models.CharField(max_length=50)
    instagram = models.CharField(max_length=50)
    twitter = models.CharField(max_length=50)
    linkedin = models.CharField(max_length=50)
    aboutus = RichTextUploadingField() # bunu yazmak için ckeditor yükledik ve import ettik.
    contact = RichTextUploadingField()
    references = RichTextUploadingField()
    status = models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True) # zamanları alıp ne zaman oluşturulduğunu biliyoruz.
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title  # admin sitesinde göstereceği

class ContactFormMessage(models.Model):
    STATUS = ( # Mesaj new, read, cloased olarak ayrılsın diye.
        ('New','New'),
        ('Read','Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True,max_length=20)
    email = models.CharField(blank=True,max_length=50)
    subject = models.CharField(blank=True,max_length=50)
    message = models.CharField(blank=True,max_length=255)
    status = models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True,max_length=20)
    note = models.CharField(blank=True,max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ContactFormu(ModelForm): # burada iletişim.py da oluşturulan sitenin mesaj gönderme kısmının nasıl olacağı
    # temeli yazılmıştır.
    class Meta:
        model =ContactFormMessage
        fields = ['name','email','subject','message']
        widgets = {
            'name' : TextInput(attrs={'class': 'form-control','placeholder':'Name & Surname'}),
            'subject' : TextInput(attrs={'class': 'form-control','placeholder':'Subject'}),
            'email' : TextInput(attrs={'class': 'form-control','placeholder':'Email Address'}),
            'message' : Textarea(attrs={'class': 'form-control','placeholder':'Your Message' }),
        }

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank= True, max_length=20)
    address = models.CharField(blank= True, max_length=20)
    city = models.CharField(blank= True, max_length=20)
    country = models.CharField(blank= True, max_length=20)
    image = models.ImageField(blank= True, upload_to='images/users/')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return '[ '+self.user.username+' ]' + '  ' + self.user.first_name+ '  '+ self.user.last_name

    def image_tag(self):
        return mark_safe('<img src ="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

class UserProfileForm(ModelForm):  # burada iletişim.py da oluşturulan sitenin mesaj gönderme kısmının nasıl olacağı
    # temeli yazılmıştır.
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country','image']

class FAQ(models.Model) :
    STATUS = (  # seçim yapılması için
        ('True', 'Evet'),
        ('False','Hayır'),
    )
    ordernumber = models.IntegerField()
    question = models.CharField(max_length=150)
    answer = models.TextField()
    status = models.CharField(max_length=10,choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True) # zamanları alıp ne zaman oluşturulduğunu biliyoruz.
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question  # admin sitesinde göstereceği
