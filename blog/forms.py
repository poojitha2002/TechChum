from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db import models
from django.forms import ModelForm
from django.contrib.auth import authenticate, get_user_model
from .models import  Contest,ContestSubmission,CoursesForInterviews,CoursesForInterviewsContent,ContestQuestions,Resource
class ContactForm(forms.Form):
    name=forms.CharField(max_length=100)
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


class ContestStart(ModelForm):
    class Meta:
        model=Contest
        fields="__all__"

class ContestQuestionsForm(ModelForm):
    class Meta:
        model=ContestQuestions
        fields="__all__"

class ContestForm(ModelForm):
    class Meta:
        model = ContestSubmission
        fields = ['url']

class InterviewCoursesForm(ModelForm):
    class Meta:
        model=CoursesForInterviews
        fields=['courseName','image','content']

class ResourceForms(ModelForm):
    class Meta:
        model=Resource
        fields="__all__"


class CoursesForInterviewsContentForm(ModelForm):
    class Meta:
        model=CoursesForInterviewsContent
        fields=['course','day','content']

