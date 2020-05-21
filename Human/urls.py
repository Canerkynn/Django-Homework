from django.urls import path

from Human import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path('addcomment/<int:id>',views.addcomment, name='addcomment'),
    path('addcommentcontent/<int:id>',views.addcommentcontent, name='addcommentcontent'),
]