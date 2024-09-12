from django.db import models
from django.contrib.auth.models import User
from datetime import datetime,timedelta
from django.shortcuts import  redirect, reverse




class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    enrollment = models.CharField(max_length=40)
    branch = models.CharField(max_length=40)
    #used in issue book
    def __str__(self):
        return self.user.first_name+'['+str(self.enrollment)+']'
    @property
    def get_name(self):
        return self.user.first_name
    @property
    def getuserid(self):
        return self.user.id


class Book(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('history', 'History'),
        ]
    name=models.CharField(max_length=30)
    isbn=models.PositiveIntegerField()
    author=models.CharField(max_length=40)
    category=models.CharField(max_length=30,choices=catchoice,default='education')
    def __str__(self):
        return str(self.name)+"["+str(self.isbn)+']'
    
    @property
    def delete_url(self):
        url = reverse('books.delete', args=[self.id])
        return url
    @property
    def edit_url(self):
        url = reverse('books.edit',args=[self.id])
        return url


def get_expiry():
    return datetime.today() + timedelta(days=15)
class IssuedBook(models.Model):
    enrollment=models.CharField(max_length=30)
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    statuschoice= [
        ('Issued', 'Issued'),
        ('Returned', 'Returned'),
        ]
    status=models.CharField(max_length=20,choices=statuschoice,default="Issued")
    def __str__(self):
        return self.enrollment
