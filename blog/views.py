from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage
from datetime import datetime
from operator import itemgetter
from .utils import get_plot
# Import mimetypes module
import mimetypes
# import os module
import os

from .forms import ContactForm,ContestForm,InterviewCoursesForm,CoursesForInterviewsContentForm,ContestStart,ContestQuestionsForm,ResourceForms
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import requests
from .models import Courses,Memes,Scholorships,Internships,ScholorshipTrack,Fellowships,Allfiles,Goodies,Contest,ContestQuestions,ContestSubmission,CoursesForInterviews,CoursesForInterviewsContent,gifts
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_control
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post,Resource
from cart.cart import Cart

def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")


def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


def cart_detail(request):
    return render(request, 'cart/cart_detail.html')
def homepage(request):
    return render(request,'blog/homepage.html')

def home(request):

    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def rhome(request):
    user = str(request.user)
    c = 0
    print(user)
    if user == 'poojitha':
        c = 1
    context={
        'resources':Resource.objects.all(),
        'c':c
    }
    return render(request,'blog/resources.html',context)

def mock(request):
    return render(request,'blog/mock.html')

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class resourcesView(ListView):
    model=Resource
    template_name='blog/resources.html'
    context_object_name = 'resources'

class memesView(ListView):
    model=Memes
    template_name='blog/memes.html'
    context_object_name = 'memes'


class ScholorshipsView(ListView):
    model=Scholorships
    template_name = 'blog/opportunities.html'
    context_object_name = 'scholorships'

class KLHub(ListView):
    model=Courses
    template_name = 'blog/kl.html'
    context_object_name = 'courses'

def files(request,id):
    context={'id':id}
    return render(request,'blog/files.html',context)


def opportunities(request):
    scholorships=Scholorships.objects.all()
    internships=Internships.objects.all()
    fellowships=Fellowships.objects.all()
    context={'scholorships':scholorships,'internships':internships,'fellowships':fellowships}
    return render(request,'blog/opportunities.html',context)

def CoursesInterviews(request):
    user=str(request.user)
    courses=CoursesForInterviews.objects.all()
    #print("user= ",user)
    c=0
    if user=='poojitha':
        c=1
    #print(c)
    #print(type(user))
    context={'courses':courses,'c':c}
    return render(request,'blog/courses.html',context)

def showContent(request,id):
    user = str(request.user)
    content=CoursesForInterviewsContent.objects.filter(course=id)
    c = 0
    if user == 'poojitha':
        c = 1
    context={'content':content,'c':c,'id':id}
    return render(request,'blog/coursecontent.html',context)

def addCourse(request):
    if request.method=='POST':
        form=InterviewCoursesForm(request.POST,request.FILES)
        if form.is_valid():
            courseName=form.cleaned_data.get('courseName')
            image=form.cleaned_data.get('image')
            content=form.cleaned_data.get('content')
            x=CoursesForInterviews.objects.create(courseName=courseName,image=image,content=content)
            #x=CoursesForInterviews(courseName=courseName,image=image,content=content)
            x.save()

            messages.success(request,f'Your Course was Added ')
            return redirect('courses')
    else:
        form=InterviewCoursesForm()
    return render(request,'blog/addCourse.html',{'form':form})

def addContest(request):
    if request.method=='POST':
        form=ContestStart(request.POST,request.FILES)
        if form.is_valid():
            contest_name=form.cleaned_data.get('contest_name')
            tags=form.cleaned_data.get('tags')
            start=form.cleaned_data.get('start')
            end = form.cleaned_data.get('end')
            x=Contest.objects.create(contest_name=contest_name,tags=tags,start=start,end=end)
            #x=CoursesForInterviews(courseName=courseName,image=image,content=content)
            x.save()

            messages.success(request,f'Contest was Added ')
            return redirect('contests')
    else:
        form=ContestStart()
    return render(request,'blog/addContest.html',{'form':form})


def addResource(request):
    if request.method=='POST':
        print(request.POST)
        form=ResourceForms(request.POST,request.FILES)
        if form.is_valid():
            print('valid')
            courseName=form.cleaned_data.get('courseName')
            image=form.cleaned_data.get('image')
            content=form.cleaned_data.get('content')
            file = form.cleaned_data.get('file')
            x=Resource.objects.create(courseName=courseName,image=image,content=content,file=file)
            x.save()
            messages.success(request,f'Resource was Added ')
            return redirect('resources')
    else:
        print('invalid')
        form=ResourceForms()
    return render(request,'blog/addResource.html',{'form':form})



def addCourseContent(request,id):
    if request.method=='POST':
        form=CoursesForInterviewsContentForm(request.POST,request.FILES)
        if form.is_valid():
            course=form.cleaned_data.get('course')
            day=form.cleaned_data.get('day')
            content=form.cleaned_data.get('content')
            x=CoursesForInterviewsContent.objects.create(course=course,day=day,content=content)
            #x=CoursesForInterviews(courseName=courseName,image=image,content=content)
            x.save()

            messages.success(request,f'Your Content was Added ')
            return redirect('courses')
    else:
        form=CoursesForInterviewsContentForm()
    return render(request,'blog/addcoursecontent.html',{'form':form})



def addContestContent(request,id):
    if request.method=='POST':
        form=ContestQuestionsForm(request.POST,request.FILES)
        if form.is_valid():
            contest=form.cleaned_data.get('contest')
            contest_desc=form.cleaned_data.get('contest_desc')
            img=form.cleaned_data.get('img')
            x=ContestQuestions.objects.create(contest=contest,contest_desc=contest_desc,img=img)
            #x=CoursesForInterviews(courseName=courseName,image=image,content=content)
            x.save()

            messages.success(request,f' Contest Questions were Added Successfully ')
            return redirect('contests')
    else:
        form=ContestQuestionsForm()
    return render(request,'blog/addcontestcontent.html',{'form':form})



def practice(request):
    response=requests.get('https://codeforces.com/api/problemset.problems').json()
    #print(response['result'])
    stuff=response['result']['problems']
    #print(stuff[0:4])
    print(stuff[20])
    p=Paginator(stuff,10)
    if request.method=="POST":
        some_var = request.POST.getlist('checks[]')
        print("Check boxes: \n",some_var)
        ll=request.POST['ll']
        ul=request.POST['ul']
        print("ll=",ll)
        print('ul= ',ul)

        if len(ll)!=0 and len(ul)!=0:
            stuff2 = []
            for i in stuff:
                if  'rating' in i.keys()  and i['rating'] >= int(ll) and i['rating'] <=int(ul):
                    stuff2.append(i)
            p=Paginator(stuff2,10)
        else:
            p=Paginator(stuff,10)

    page_num=request.GET.get('page',1)
    try:
        page=p.page(page_num)
    except EmptyPage:
        page=p.page(1)


    context={'items':page}
    return render(request,'blog/practice.html',context)



def sortup(request):
    response=requests.get('https://codeforces.com/api/problemset.problems').json()
    #print(response['result'])

    stuff=response['result']['problems']
    ordering_fields='__all__'
    p=Paginator(stuff,10)
    print("number of pages:")
    print(p.num_pages)
    page_num=request.GET.get('page',1)
    try:
        page=p.page(page_num)
    except EmptyPage:
        page=p.page(1)
    context={'items':page}
    return render(request,'blog/practice.html',context)






def opportunitiesIntern(request):
    internships=Internships.objects.all()
    context={'internships':internships}
    return render(request,'blog/opportunities.html',context)

def Showfiles(request,id):
    allfiles=Allfiles.objects.filter(course=id)
    context={'allfiles':allfiles}
    return render(request,'blog/files.html',context)



def delete(request,id):
    i=CoursesForInterviews.objects.filter(pk=id).delete()
    courses = CoursesForInterviews.objects.all()
    messages.success(request, f'Your Course was deleted successfully ')
    context = {'courses': courses }
    return redirect('courses')

def deletecontent(request,id):
    i=CoursesForInterviewsContent.objects.filter(pk=id).delete()
    messages.success(request, f'Your Course content was deleted successfully ')
    return redirect('showContent',id)


def contests(request):
    cont=Contest.objects.all()
    user = str(request.user)
    c = 0
    if user == 'poojitha':
        c = 1
    context={'cont':cont,'c':c}
    return render(request,'blog/contests.html',context)

def contestDesc(request,id):
    user = str(request.user)

    c1 = 0
    if user == 'poojitha':
        c1 = 1
    desc=ContestQuestions.objects.filter(contest=id)
    obj = Contest.objects.get(pk=id)
    c=0
    if obj.start.replace(tzinfo=None) <= datetime.now().replace(tzinfo=None) <= obj.end.replace(tzinfo=None):
        c=1
    print(c)
    context={'desc':desc,'c':c,'c1':c1,'id':id}
    return render(request,'blog/contestDesc.html',context)


def addurl(request):
    if request.method=='POST':
        form=ContestForm(request.POST)
        if form.is_valid():
            current_user = request.user
            print(current_user)

            url=form.cleaned_data.get('url')
            x=ContestSubmission(author=current_user,url=url)
            x.save()

            messages.success(request,f'Your Submission was recorded ')
            return redirect('thankyou')
    else:
        form=ContestForm()
    return render(request,'blog/submit.html',{'form':form})

def thankyou(request):
    return render(request,'blog/thanks.html')



def goodies(request):
    vouchers = gifts.objects.all()
    current_user = request.user

    print(vouchers)
    print(current_user.username)
    good=Goodies.objects.filter(author=current_user.username)
    print(good)
    context={'good':good,'vouchers':vouchers}

    return render(request,'blog/goodies.html',context)


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class GoodiesView:
    model=Goodies
    template_name='blog/goodies.html'
    context_object_name='goodies'

    def get_queryset(self):
        user=get_object_or_404(User,username=self.kwargs.get('username'))
        return Goodies.objects.filter(author=user)

class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def paint(request):
    return render(request,'blog/paint.html');
def courses(request):
    return render(request,'blog/courses.html');


def contact(request):

	if request.method == 'POST':
		message = request.POST['message']

		send_mail('Contact Form',message, settings.EMAIL_HOST_USER,['ravuri.poojitha123@gmail.com'], fail_silently=False)
	return render(request, 'blog/contactus.html')



def viewScholorships(request):

    return render(request,'blog/opportunities.html',{'jlist':ScholorshipTrack.objects.all()})


def leaderboard(request):
    levelscore=Level.objects.all().order_by('-score')
    return render(request,'leaderboard.html',{'levelscore':levelscore })