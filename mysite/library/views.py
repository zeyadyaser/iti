from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from . import forms,models
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib import auth
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.views.generic import  UpdateView, DeleteView
from librarymanagement.settings import EMAIL_HOST_USER
from .models import Book
from .forms import BookForm

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/index.html')

def logout(request):
    return render(request,'library/index.html')

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/studentclick.html')

#for showing signup/login button for admin
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'library/adminclick.html')









def studentsignup_view(request):
    form=forms.StudentUserForm()
    mydict={'form':form}
    if request.method=='POST':
        form=forms.StudentUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('studentlogin')
    return render(request,'library/studentsignup.html',context=mydict)




def is_admin(user):
    if user.is_superuser or user.is_staff:
        return True
    else:
        return False

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()
def afterlogin_view(request):
    if is_admin(request.user):
        return render(request,'library/adminafterlogin.html')
    
    elif(is_student(request.user)):
        return render(request,'library/studentafterlogin.html')


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    form=forms.BookForm()
    if request.method=='POST':
        form=forms.BookForm(request.POST)
        if form.is_valid():
            user=form.save()
            return render(request,'library/bookadded.html')
    return render(request,'library/addbook.html',{'form':form})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewbook_view(request):
    books=models.Book.objects.all()
    return render(request,'library/viewbook.html',{'books':books})





def issuebook_view(request):
    form=forms.IssuedBookForm()
    if request.method=='POST':
        form=forms.IssuedBookForm(request.POST)
        if form.is_valid():
            obj=models.IssuedBook()
            obj.enrollment=request.POST.get('enrollment2')
            obj.isbn=request.POST.get('isbn2')
            obj.save()
            return render(request,'library/bookissued.html')
    return render(request,'library/issuebook.html',{'form':form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewissuedbook_view(request):
    issuedbooks=models.IssuedBook.objects.all()
    li=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(models.Book.objects.filter(isbn=ib.isbn))
        students=list(models.StudentExtra.objects.filter(enrollment=ib.enrollment))
        i=0
        for l in books:
            t=(students[i].get_name,students[i].enrollment,books[i].name,books[i].author,issdate,expdate,fine,ib.status)
            i=i+1
            li.append(t)

    return render(request,'library/viewissuedbook.html',{'li':li})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def viewstudent_view(request):
    students=models.StudentExtra.objects.all()
    return render(request,'library/viewstudent.html',{'students':students})


@login_required(login_url='studentlogin')
def viewissuedbookbystudent(request):
    student=models.StudentExtra.objects.filter(user_id=request.user.id)
    issuedbook=models.IssuedBook.objects.filter(enrollment=student[0].enrollment)

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=models.Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,student[0].branch,book.name,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine,ib.status,ib.id)
        li2.append(t)

    return render(request,'library/viewissuedbookbystudent.html',{'li1':li1,'li2':li2})
def returnbook(request, id):
    issued_book = models.IssuedBook.objects.get(pk=id)
    issued_book.status = "Returned"
    issued_book.save()
    return redirect('viewissuedbookbystudent')


def aboutus(request):
    return render(request,'library/aboutus.html')

def contactus(request):
    return render(request,'library/contactus.html')


class DeleteBook(DeleteView):
    model = Book
    success_url = "/viewbook"
    
class UpdateBook(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'library/edit.html'
    success_url = "/viewbook"