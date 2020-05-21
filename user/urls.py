from django.urls import path

from user import views

urlpatterns = [
    path('', views.index,name='index'),
    path('update/',views.user_update, name='user_update'),
    path('password/',views.change_password, name='user_password'),
    path('comments/',views.comments, name='comments'),
    path('deletecomment/<int:id>',views.deletecomment, name='deletecomment'),
    path('addcontent/',views.addcontent, name='addcontent'),
    path('addposts/',views.addposts, name='addposts'),
    path('contents/',views.contents, name='contents'),
    path('posts/',views.posts, name='posts'),
    path('contentedit/<int:id>',views.contentedit, name='contentedit'),
    path('postsedit/<int:id>',views.postsedit, name='postsedit'),
    path('contentdelete/<int:id>',views.contentdelete, name='contentdelete'),
    path('postsdelete/<int:id>',views.postsdelete, name='postsdelete'),
    path('adduserprofile/',views.adduserprofile, name='adduserprofile'),
    path('myposts/', views.myposts, name='myposts'),
    path('contentaddimage/<int:id>', views.contentaddimage, name='contentaddimage'),
    path('productaddimage/<int:id>', views.productaddimage, name='productaddimage'),

]