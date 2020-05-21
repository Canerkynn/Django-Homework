from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from Human.models import CommentForm, Comment, CommentContent


def index(request):
    text = "Merhaba Django"
    context = {'text' : text}
    return render(request,'index.html',context)

def addcomment(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user
            data = Comment()
            data.user_id = current_user.id
            data.product_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Yorumunuz başarı ile gönderilmiştir. Teşekkür Ederiz.')
            return HttpResponseRedirect(url)
    messages.warning(request, 'Yorumunuz başarız oldu. Lütfen kontrol edin.')
    return HttpResponseRedirect(url)

def addcommentcontent(request,id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user
            data = CommentContent()
            data.user_id = current_user.id
            data.content_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, 'Yorumunuz başarı ile gönderilmiştir. Teşekkür Ederiz.')
            return HttpResponseRedirect(url)
    messages.warning(request, 'Yorumunuz başarız oldu. Lütfen kontrol edin.')
    return HttpResponseRedirect(url)