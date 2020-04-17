from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here
from Human.models import Product, Categories, Images
from home.models import Setting, ContactFormu, ContactFormMessage


def index (request):
    setting =Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()
    category = Categories.objects.all()
    dayphoto = Product.objects.all()[:3]
    lastphotos = Product.objects.all().order_by('-id')[:3]
    randomphotos = Product.objects.all().order_by('?')[:3]
    context = {'setting': setting,
               'page':'home',
               'sliderdata':sliderdata,
               'category':category,
               'dayphoto':dayphoto,
               'lastphotos':lastphotos,
               'randomphotos':randomphotos,
               }
    return render(request,'index.html',context)


def hakkimizda (request):
    setting =Setting.objects.get(pk=1)
    context = {'setting': setting, 'page':'hakkimizda'}
    return render(request,'hakkimizda.html',context)

def referanslarimiz (request):
    setting =Setting.objects.get(pk=1)
    context = {'setting': setting, 'page':'referanslarimiz'}
    return render(request,'referanslarimiz.html',context)

def iletisim (request):
    if request.method == 'POST': #form post edildiyse
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage() # model ile bağlantı kur
            data.name = form.cleaned_data['name'] # fromdan bilgileri al
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip =request.META.get('REMOTE_ADDR')
            data.save() # veriyi kaydet
            messages.success(request,"Messajınız başarı ile gönderilmiştir. Teşekkür Ederiz")
            return HttpResponseRedirect('/iletisim')
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'form':form, 'page':'iletisim'}
    return render(request,'iletisim.html',context)

def category_products(request,id,slug):
    category = Categories.objects.all()
    categorydata = Categories.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products' : products,
               'category' : category,
               'categorydata' : categorydata,}
    return render(request, 'product.html', context)


def product_detail(request,id,slug):
    category = Categories.objects.all()
    product = Product.objects.get(pk=id)
    photos = Images.objects.filter(photo_id=id)
    context= {'category' : category,
              'product' : product,
              'photos' : photos,}
    return render(request, 'product_detail.html',context)