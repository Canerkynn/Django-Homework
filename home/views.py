from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here
from Human.models import Product
from home.models import Setting


def index (request):
    setting =Setting.objects.get(pk=1)
    context = {'setting': setting}
    return render(request,'index.html',context)

