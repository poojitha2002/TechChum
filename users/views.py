from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from blog.models import Goodies,ContestSubmission,clgModel
from .models import UserDummy,Ratings
from .utils import get_plot
from django.conf import settings
from django.core.mail import send_mail
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            clg=form.cleaned_data.get('clg')
            print(clg)
            b=Goodies(coins=0,author=username)
            b.save()
            u=UserDummy(author=username)
            u.save()
            messages.success(request, f'Your account has been created! You are now able to log in')
            subject = 'Welcome to TechChum'
            message = f'Hello {username}!\nYou have successfully created a TechChum account.Thank you for teaming up with us, the best place to prepare for your dream Tech job.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, email_from, recipient_list)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    current_user = request.user
    print(current_user)
    place = UserDummy.objects.get(author=current_user)
    print(current_user)
    qs = Ratings.objects.filter(author=place)
    print(qs)
    x = [x.contest for x in qs]
    y = [y.rating for y in qs]
    chart = get_plot(x, y)
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'chart':chart,
    }

    return render(request, 'users/profile.html', context)
def ratings_view(request,id):
    current_user=request.user
    qs=Ratings.objects.filter(author=id)
    print(qs)
    x=[x.contest for x in qs]
    y=[y.rating for y in qs]
    chart=get_plot(x,y)
    return render(request,'users/profile.html',{'chart':chart})