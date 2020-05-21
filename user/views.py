from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from Human.models import Categories, Comment, ProductForm, Product, CommentContent, ProductImageForm, Images
from content.models import Menu, Content, ContentForm, CImages, ContentImageForm
from home.models import UserProfile, UserProfileForm, Setting
from user.forms import UserUpdateForm, ProfileUpdateForm

def index(request):
    setting = Setting.objects.get(pk=1)
    category = Categories.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id = current_user.id)
    context = {
        'category' : category,
        'profile' : profile,
        'setting': setting,
        }
    return render(request,'user_profile.html',context)

def user_update(request):
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.userprofile )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/user')
    else:
        category = Categories.objects.all()
        user_form = UserUpdateForm(instance = request.user)
        profile_form = ProfileUpdateForm(instance = request.user.userprofile)
        context = {
            'category' : category,
            'user_form' : user_form,
            'profile_form' : profile_form,
            'profile' : profile,
            'setting' : setting,
        }
        return render(request, 'user_update.html', context)

def change_password(request):
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,'Your password was succesfully updated!')
            return redirect('/user')
        else:
            messages.warning(request,'Please correct the error below.' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        category = Categories.objects.all()
        form = PasswordChangeForm(request.user)
        return render(request, 'change_password.html',
                      {'form': form,
                       'category': category,
                       'profile' : profile,
                       'setting' : setting
                       })

@login_required(login_url='/login')
def comments(request):
    setting = Setting.objects.get(pk=1)
    current_user =request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    menu = Menu.objects.all()
    comments = Comment.objects.filter(user_id = current_user.id)
    commentscontent = CommentContent.objects.filter(user_id = current_user.id)
    context = {
        'comments' : comments,
        'profile' : profile,
        'menu' : menu,
        'commentscontent' : commentscontent,
        'setting' : setting,
    }
    return render(request, 'user_comments.html', context)

@login_required(login_url='/login')
def deletecomment(request,id):
    current_user=request.user
    Comment.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request,'Comment deleted...')
    return HttpResponseRedirect('/user/comments')

@login_required(login_url='/login')
def addcontent(request):
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Content()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.type = form.cleaned_data['type']
            data.slug = form.cleaned_data['slug']
            data.detail = form.cleaned_data['detail']
            data.status = 'False'
            data.save()
            messages.success(request,'Your Content Inserted Succesfully')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(request, 'Content Form Error : '+ str(form.errors))
            return HttpResponseRedirect('/user/addcontent')
    else:
        category = Categories.objects.all()
        menu = Menu.objects.all()
        form = ContentForm()
        context = {
            'category': category,
            'menu': menu,
            'form': form,
            'profile' : profile,
            'setting' : setting,
        }
        return render(request, 'user_addcontent.html', context)

@login_required(login_url='/login')
def contents(request):
    setting = Setting.objects.get(pk=1)
    category = Categories.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    contents = Content.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'menu': menu,
        'contents': contents,
        'profile' : profile,
        'setting' : setting,
    }
    return render(request, 'user_contents.html', context)

@login_required(login_url='/login')
def contentdelete(request,id):
    current_user = request.user
    Content.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Content deleted...')
    return HttpResponseRedirect('/user/contents')

@login_required(login_url='/login')
def contentedit(request,id):
    setting = Setting.objects.get(pk=1)
    content = Content.objects.get(id=id)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES,instance=content)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Content Updated Succesfully')
            return HttpResponseRedirect('/user/contents')
        else:
            messages.success(request, 'Content Form Error : ' + str(form.errors))
            return HttpResponseRedirect('/user/contentedit/'+str(id))
    else:
        category = Categories.objects.all()
        menu = Menu.objects.all()
        form = ContentForm(instance=content)
        context = {
            'category': category,
            'menu': menu,
            'form': form,
            'profile' : profile,
            'setting' : setting,
        }
        return render(request, 'user_addcontent.html', context)

@login_required(login_url='/login')
def adduserprofile(request):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        form2 = UserProfileForm(request.POST, request.FILES)
        if form2.is_valid():
            current_user = request.user
            data2 = UserProfile()
            data2.user_id = current_user.id
            data2.phone = form2.cleaned_data['phone']
            data2.address = form2.cleaned_data['address']
            data2.city = form2.cleaned_data['city']
            data2.country = form2.cleaned_data['country']
            data2.image = form2.cleaned_data['image']
            data2.save()
            messages.success(request,'Your Content Inserted Succesfully')
            return HttpResponseRedirect('/user')
        else:
            messages.warning(request, 'Content Form Error : '+ str(form2.errors))
            return HttpResponseRedirect('/user/useraddprofile')
    else:
        category = Categories.objects.all()
        menu = Menu.objects.all()
        form = UserProfileForm()
        context = {
            'category': category,
            'menu' : menu,
            'form' : form,
            'setting' : setting,
        }
        return render(request, 'user_userprofile.html', context)

@login_required(login_url='/login')
def addposts(request):
    setting = Setting.objects.get(pk=1)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Product()
            data.user_id = current_user.id
            data.category = form.cleaned_data['category']
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.keywords = form.cleaned_data['keywords']
            data.image = form.cleaned_data['image']
            data.detail = form.cleaned_data['detail']
            data.slug = form.cleaned_data['slug']
            data.status = 'False'
            data.save()
            messages.success(request,'Your Product Inserted Succesfully')
            return HttpResponseRedirect('/user/posts')
        else:
            messages.warning(request, 'Product Form Error : '+ str(form.errors))
            return HttpResponseRedirect('/user/addposts')
    else:
        category = Categories.objects.all()
        menu = Menu.objects.all()
        form = ProductForm()
        messages.warning(request, 'Slug kısmı "username-title" şeklinde olmalıdır.')
        context = {
            'category' : category,
            'menu' : menu,
            'form' : form,
            'profile' : profile,
            'setting' : setting,
        }
        return render(request, 'user_addproduct.html', context)

@login_required(login_url='/login')
def postsedit(request,id):
    setting = Setting.objects.get(pk=1)
    product = Product.objects.get(id=id)
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Product Updated Succesfully')
            return HttpResponseRedirect('/user/posts')
        else:
            messages.success(request, 'Product Form Error : ' + str(form.errors))
            return HttpResponseRedirect('/user/postedit/'+str(id))
    else:
        category = Categories.objects.all()
        menu = Menu.objects.all()
        form = ProductForm(instance=product)
        messages.warning(request, 'Slug kısmı "username-title" şeklinde olmalıdır.')
        context = {
            'category': category,
            'menu': menu,
            'form': form,
            'profile' : profile,
            'setting' : setting,
        }
        return render(request, 'user_addproduct.html', context)

@login_required(login_url='/login')
def postsdelete(request,id):
    current_user = request.user
    Product.objects.filter(id=id, user_id=current_user.id).delete()
    messages.success(request, 'Posts deleted...')
    return HttpResponseRedirect('/user/posts/')

@login_required(login_url='/login')
def posts(request):
    setting = Setting.objects.get(pk=1)
    category = Categories.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    product = Product.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'menu': menu,
        'contents': contents,
        'profile' : profile,
        'product' : product,
        'setting' : setting,
    }
    return render(request, 'user_posts.html', context)

@login_required(login_url='/login')
def myposts(request):
    setting = Setting.objects.get(pk=1)
    category = Categories.objects.all()
    menu = Menu.objects.all()
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    product = Product.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'menu': menu,
        'contents': contents,
        'profile': profile,
        'product': product,
        'setting': setting,
        'page':'gallery',
    }
    return render(request, 'myPosts.html', context)

def contentaddimage(request, id):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = ContentImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = CImages()
            data.title = form.cleaned_data['title']
            data.content_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your image has been successfully uploaded')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error :', + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        content = Content.objects.get(id=id)
        images = CImages.objects.filter(content_id=id)
        form = ContentImageForm()
        context = {
            'content': content,
            'images': images,
            'form': form,
            'setting' : setting,
        }
        return render(request, 'content_gallery.html', context)

def productaddimage(request, id):
    setting = Setting.objects.get(pk=1)
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.title = form.cleaned_data['title']
            data.photo_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Your image has been successfully uploaded')
            return HttpResponseRedirect(lasturl)
        else:
            return HttpResponseRedirect(lasturl)
    else:
        product = Product.objects.get(id=id)
        images = Images.objects.filter(photo_id=id)
        form = ProductImageForm()
        context = {
            'product' : product,
            'images' : images,
            'form' : form,
            'setting' : setting,
        }
        return render(request, 'product_gallery.html', context)