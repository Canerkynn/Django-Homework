from django.contrib import messages
import json

from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here
from Human.models import Product, Categories, Images, Comment
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage


def index(request):
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
    context = {'setting': setting,
               'page':'referanslarimiz'}
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
    comments = Comment.objects.filter(product_id=id, status='True')
    context= {'category' : category,
              'product' : product,
              'photos' : photos,
              'comments':comments,
              }
    return render(request, 'product_detail.html',context)


def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Categories.objects.all()

            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                products = Product.objects.filter(title__icontains=query)
            else:
                products = Product.objects.filter(title__icontains=query,category_id=catid)
            context= {'products':products,
                      'category':category,}
            return render(request,'products_search.html',context)

    return HttpResponseRedirect('/')


def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login (request,user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Login Hatası ! Kullanıcı adı yada şifre hatalı ")
            return HttpResponseRedirect('/login')
    category = Categories.objects.all()
    context = {'category': category, }
    return render(request, 'login.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Hata oluştu ! Doldurulması gereken alanları doldurun ve şifreyi kurallara göre oluşturun..! ")
            return HttpResponseRedirect('/signup')

    form = SignUpForm()
    category = Categories.objects.all()
    context = {'category': category,
               'form' : form,
               }
    return render(request, 'signup.html', context)
