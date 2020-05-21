from django.contrib import messages
import json

from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here
from Human.models import Product, Categories, Images, Comment, CommentContent
from content.models import Content, CImages, Menu
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile, FAQ


def index(request):
    setting =Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()
    category = Categories.objects.all()
    menu = Menu.objects.all()
    dayphoto = Product.objects.filter(status='True')[:3]
    lastphotos = Product.objects.filter(status='True').order_by('-id')[:3]
    randomphotos = Product.objects.filter(status='True').order_by('?')[:3]
    news = Content.objects.filter(type='haber',status='True').order_by('-id')[:3]
    announcements = Content.objects.filter(type='duyuru',status='True').order_by('-id')[:3]
    current_user = request.user
    userProfile = UserProfile.objects.all()
    if current_user.id != None :
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'setting': setting,
                   'page':'home',
                   'sliderdata':sliderdata,
                   'category':category,
                   'dayphoto':dayphoto,
                   'lastphotos':lastphotos,
                   'randomphotos':randomphotos,
                   'news' : news,
                   'menu' : menu,
                   'announcements' : announcements,
                   'profile':profile,
                   'userProfile' : userProfile,
                   }
        return render(request,'index.html',context)
    else:
        context = {'setting': setting,
                   'page': 'home',
                   'sliderdata': sliderdata,
                   'category': category,
                   'dayphoto': dayphoto,
                   'lastphotos': lastphotos,
                   'randomphotos': randomphotos,
                   'news': news,
                   'menu': menu,
                   'announcements': announcements,
                   }
        return render(request, 'index.html', context)

def hakkimizda (request):
    setting =Setting.objects.get(pk=1)
    current_user = request.user
    if current_user.id != None:
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'setting': setting,
                   'page':'hakkimizda',
                   'profile':profile,
                   }
        return render(request,'hakkimizda.html',context)
    else:
        context = { 'setting': setting,
                    'page':'hakkimizda',
                    }
        return render(request,'hakkimizda.html',context)

def referanslarimiz (request):
    setting =Setting.objects.get(pk=1)
    current_user = request.user
    if current_user.id != None:
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'setting': setting,
                   'page': 'referanslarimiz',
                   'profile': profile,
                   }
        return render(request, 'referanslarimiz.html', context)
    else:
        context = {'setting': setting,
                   'page': 'referanslarimiz',
                   }
        return render(request, 'referanslarimiz.html', context)

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

    current_user = request.user
    if current_user.id != None:
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'setting': setting,
                   'page': 'iletisim',
                   'profile': profile,
                   'form': form,
                   }
        return render(request, 'iletisim.html', context)
    else:
        context = {'setting': setting,
                   'page': 'iletisim',
                   'form': form,
                   }
        return render(request, 'iletisim.html', context)

def category_products(request,id,slug):
    setting = Setting.objects.get(pk=1)
    category = Categories.objects.all()
    categorydata = Categories.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products' : products,
               'category' : category,
               'categorydata' : categorydata,
               'setting' : setting,}
    return render(request, 'product.html', context)

def product_detail(request,id,slug):
    setting = Setting.objects.get(pk=1)
    category = Categories.objects.all()
    try:
        product = Product.objects.get(pk=id)
        photos = Images.objects.filter(photo_id=id)
        comments = Comment.objects.filter(product_id=id, status='True')
        current_user = request.user
        if current_user.id != None:
            profile = UserProfile.objects.get(user_id=current_user.id)
            context = {'category' : category,
                       'photos' : photos,
                       'product' : product,
                       'comments' : comments,
                       'profile': profile,
                       'setting': setting,
                       }
            return render(request, 'product_detail.html', context)
        else:
            context = {'category' : category,
                       'photos' : photos,
                       'product': product,
                       'comments' : comments,
                       'setting' : setting,
                       }
            return render(request, 'product_detail.html', context)
    except:
        messages.warning(request,"Hata ! İlgili içerik bulunamadı...")
        link='/error'
        return HttpResponseRedirect(link)

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
    setting = Setting.objects.get(pk=1)
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
    context = {'category': category,'setting':setting }
    return render(request, 'login.html', context)

def signup_view(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, " Kayıt oldunuz... Profilinizi oluşturmanız gerekmekte lütfen Oluşturun..! ")
            return HttpResponseRedirect('/user/adduserprofile')
        else:
            messages.warning(request, "Hata oluştu ! Doldurulması gereken alanları doldurun ve şifreyi kurallara göre oluşturun..! ")
            return HttpResponseRedirect('/signup')
    form = SignUpForm()
    category = Categories.objects.all()
    context = {'category': category,
               'form' : form,
               'setting':setting,
               }
    return render(request, 'signup.html', context)

def content_detail(request,id,slug):
    setting = Setting.objects.get(pk=1)
    category = Categories.objects.all()
    menu = Menu.objects.all()
    try:
        content = Content.objects.get(pk=id)
        images = CImages.objects.filter(content_id=id)
        comments = CommentContent.objects.filter(content_id=id)
        context = {'category': category,
                   'menu': menu,
                   'content': content,
                   'images': images,
                   'comments':comments,
                   'setting':setting,
                   }
        return render(request, 'content_detail.html', context)
    except:
        messages.warning(request,"Hata ! İlgili içerik bulunamadı...")
        link='/error'
        return HttpResponseRedirect(link)

def menu(request,id):
    try:
        content = Content.objects.get(menu_id=id)
        link ='/content/'+str(content.id)+'/menu'
        return HttpResponseRedirect(link)
    except:
        messages.success(request, "Hata ! ilgili içerik bulunamadı")
        link='/error'
        return HttpResponseRedirect(link)

def error(request):
    setting = Setting.objects.get(pk=1)
    category = Categories.objects.all()
    menu = Menu.objects.all()
    context = {
        'category': category,
        'menu' : menu,
        'setting' : setting,
    }
    return render(request,'error_page.html',context)

def faq(request):
    setting =Setting.objects.get(pk=1)
    category = Categories.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    faq = FAQ.objects.all().order_by('ordernumber')
    if current_user.id != None:
        profile = UserProfile.objects.get(user_id=current_user.id)
        context = {'category': category,
                   'menu': menu,
                   'faq': faq,
                   'profile': profile,
                   'page' : 'sss',
                   'settinng' : setting,
                   }
        return render(request, 'faq.html', context)
    else:
        context = {'category': category,
                   'menu': menu,
                   'faq': faq,
                   'page': 'sss',
                   'settinng': setting,
                   }
        return render(request, 'faq.html', context)