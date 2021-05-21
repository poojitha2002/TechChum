from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField

class Resource(models.Model):
    courseName = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg')
    content = models.TextField(default='Content to be displayed')
    file = models.FileField()

    def __str__(self):
        return self.courseName

class Memes(models.Model):
    image = models.ImageField(default='default.jpg')

class Scholorships(models.Model):
    url=models.URLField(max_length=1000)

class Fellowships(models.Model):
    url=models.URLField(max_length=1000)

class Internships(models.Model):
    url=models.URLField(max_length=500)

class ScholorshipTrack(models.Model):
    name=models.CharField(max_length=40)
    url=models.URLField(max_length=500)

    def __str__(self):
        return self.name


class Courses(models.Model):
    courseName = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg')
    content = models.TextField(default='Content to be displayed')

    def __str__(self):
        return self.courseName


class Allfiles(models.Model):
    course=models.ForeignKey(Courses,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    content=models.CharField(default='Content to be displayed',max_length=200)
    file=models.FileField()
    def __str__(self):
        return self.title

class CoursesForInterviews(models.Model):
    courseName = models.CharField(max_length=200)
    image = models.ImageField(default='default.jpg')
    content = models.TextField(default='Content to be displayed')

    def __str__(self):
        return self.courseName

class CoursesForInterviewsContent(models.Model):
    course = models.ForeignKey(CoursesForInterviews, on_delete=models.CASCADE)
    day=models.CharField(default='Day 1',max_length=100)
    content=RichTextField()
    def __str__(self):
        return self.day

class clgModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,default='author')
    clg=models.CharField(max_length=100)
    def __str__(self):
        return self.author




class Contest(models.Model):
    contest_name=models.CharField(max_length=100)
    tags=models.CharField(max_length=100)
    start=models.DateTimeField()
    end=models.DateTimeField()

    def __str__(self):
        return self.contest_name

class ContestQuestions(models.Model):
    contest=models.ForeignKey(Contest,on_delete=models.CASCADE)
    contest_desc=models.TextField()
    img=models.ImageField(default='default.jpg')


    def __str__(self):
        return self.contest_desc


class Goodies(models.Model):
    coins=models.IntegerField(default=0)
    author=models.CharField(max_length=300)
    def __str__(self):
        return self.author

class ContestSubmission(models.Model):
    author=models.CharField(max_length=300,primary_key=True)
    url=models.URLField()

    def __str__(self):
        return self.author

class Codeforces(models.Model):
    author=models.CharField(max_length=100)
    cfhandle=models.CharField(max_length=100)

    def __str__(self):
        return self.author

class gifts(models.Model):
    title=models.CharField(max_length=100,default='Amazon Voucher worth')
    image=models.ImageField(default='default.jpg')
    coins=models.IntegerField(default=0)
    content=models.TextField()
    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
