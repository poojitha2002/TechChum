from django.conf.urls import url
from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    resourcesView,
    KLHub,
memesView,
ScholorshipsView,
Internships
)
from . import views
from .views import *
urlpatterns = [
    path('discussionforum/', PostListView.as_view(), name='blog-home'),
    url(r'^user/(?P<username>\w{0,50})/$', UserPostListView.as_view(), name='user-posts'),

    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
   #path('goodies/',views.goodies,name='goodies'),
    path('',views.homepage,name='homepage'),
path('opportunities',views.opportunities,name='opp'),
path('internships',views.opportunitiesIntern,name='in'),
    path('mockInterviews/', views.mock, name='mock'),
    path('courses/', views.CoursesInterviews, name='courses'),
    path('paint/', views.paint, name='paint'),
    path('contact/',views.contact,name='contact'),

    path('resources/', views.rhome, name='resources'),
    path('memes/', memesView.as_view(), name='memes'),
    path('scholorships/',ScholorshipsView.as_view(),name='scholorships'),
    url(r'^files/(?P<id>\d+)/$',views.Showfiles,name='Showfiles'),
    url(r'^delete/(?P<id>\d+)/$', views.delete, name='delete'),
    url(r'^deleteContent/(?P<id>\d+)/$', views.deletecontent, name='deletecontent'),
    url(r'^showContent/(?P<id>\d+)/$', views.showContent, name='showContent'),
    url(r'^addCourseContent/(?P<id>\d+)/$',views.addCourseContent,name='addCourseContent'),


    url(r'^addContestContent/(?P<id>\d+)/$', views.addContestContent, name='addContestContent'),
    url(r'^contestDesc/(?P<id>\d+)/$', views.contestDesc, name='contestDesc'),

    path('goodies/', views.goodies, name='goodies'),
    path('KL-Hub/', KLHub.as_view(), name='klu'),
    path('<id>',views.files,name='files'),
path('contests/',views.contests,name='contests'),
    path('practice/',views.practice,name='practice'),
path('submit/',views.addurl,name='submit'),
    path('addCourse/',views.addCourse,name='addCourse'),
path('addContest/',views.addContest,name='addContest'),
path('addResource/',views.addResource,name='addResource'),



path('thankyou/',views.thankyou,name='thankyou'),
    path('sortup/', views.sortup, name='sortup'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
]
