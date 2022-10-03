from django.shortcuts import render,redirect,HttpResponse
from django.views.generic.base import View,TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import User,Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from .models import StudentExtra,Book,IssuedBook
from django.core.mail import send_mail,EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages

from . tokens import generate_token
from datetime import date
from django.views.generic.edit import UpdateView
from .forms import SearchForm,AdminSignupForm,StudentExtraForm,StudentUserForm,BookForm,IssuedBookForm,ContactusForm


# Create your views here.
class HomeTemplateView(TemplateView):
    template_name="library/index.html"

class ProfileTemplateView(TemplateView):
    template_name="library/postlogin.html"


class AdminSignupView(View):

    def post(self,request):
        if request.method == 'POST':
            form = AdminSignupForm(request.POST)
            if form.is_valid():
                username = request.POST['username']
                email = request.POST['email']
                if User.objects.filter(username=username):
                    messages.error(request, "username already exist! Please Try other username")
                    return redirect("library:home")
                if User.objects.filter(email=email):
                    messages.error(request, "email already registered")
                    return redirect("library:home")
                user = form.save()
                user.set_password(user.password)
                user.save()
                my_admin_group = Group.objects.get_or_create(name='ADMIN')
                my_admin_group[0].user_set.add(user)
             
                user.is_active = False
                              
                # welcome email
                subject = "welcome to django login"
                message = "hello " + user.first_name + "!! \n" + \
                    "welcome to authnication app!! \n Thank you for visiting our website \n we have also sent you a confirmation email,please confirm your email address in order to activate your account"
                from_email = "info@exmaple.com"
                to_list = [user.email]
                send_mail(subject, message, from_email,
                        to_list, fail_silently=True)
                #email address confirmation
                current_site = get_current_site(request)
                email_subject = "Confirm your email"
                message2 = render_to_string("email_confirmation.html", {
                    'name': user.first_name,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user),
                })
                email = EmailMessage(
                    email_subject,
                    message2,
                    from_email,
                    [user.email]
                )
                email.fail_silently = True
                email.send()
                messages.success(request, "your account has been successfully created")


            return redirect('library:home')



    def get(self,request):
        form=AdminSignupForm()
        return render(request,"library/adminsignupform.html",{'form':form})

class StudentSignupView(View):
    def post(self,request):
        if request.method == 'POST':
            form1 = StudentUserForm(request.POST)
            form2 = StudentExtraForm(request.POST)
            if form1.is_valid() and form2.is_valid():
                username = request.POST['username']
                email = request.POST['email']
                if User.objects.filter(username=username):
                    messages.error(
                        request, "username already exist! Please Try other username")
                    return redirect("library:home")
                if User.objects.filter(email=email):
                    messages.error(request, "email already registered")
                    return redirect("library:home")
                user = form1.save()
                user.set_password(user.password)
                user.save()
                f2 = form2.save(commit=False)
                f2.user = user
                user2 = f2.save()

                my_student_group = Group.objects.get_or_create(name='STUDENT')
                my_student_group[0].user_set.add(user)
                user.is_active = False
                # welcome email
                subject = "welcome to django login"
                message = "hello " + user.first_name + "!! \n" + \
                    "welcome to authnication app!! \n Thank you for visiting our website \n we have also sent you a confirmation email,please confirm your email address in order to activate your account"
                from_email = "info@exmaple.com"
                to_list = [user.email]
                send_mail(subject, message, from_email,
                          to_list, fail_silently=True)
                #email address confirmation
                current_site = get_current_site(request)
                email_subject = "Confirm your email"
                message2 = render_to_string("email_confirmation.html", {
                    'name': user.first_name,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user),
                })
                email = EmailMessage(
                    email_subject,
                    message2,
                    from_email,
                    [user.email]
                )
                email.fail_silently = True
                email.send()
                messages.success(
                    request, "your account has been successfully created")


            return redirect('library:home')
    def get(self,request):
        form1 = StudentUserForm(request.POST)
        form2 = StudentExtraForm(request.POST)
        return render(request, 'library/studentsignup.html', {'form1':form1, "form2":form2})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None
    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        return redirect("library:login")
    else:
        return render(request, "activation_failed.html")


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


def postlogin_view(request):
    if is_admin(request.user):
        myuser=User.objects.get(pk=request.user.id)
        
        return render(request, 'library/adminpostlogin.html',{"myuser":myuser})
    else:
        myuser = User.objects.get(pk=request.user.id)
        return render(request, 'library/studentpostlogin.html', {"myuser": myuser})




class CreateBookView(CreateView):

    model=Book
    fields=['name', 'isbn', 'author', 'category']
    template_name='library/book_form.html'

class TemplateBookAddedView(TemplateView):

    template_name="library/bookadded.html"

class ListBookView(ListView):
    model=Book
    context_object_name="books"

class ListStudentView(ListView):
    model=StudentExtra
    context_object_name="students"

class IssueBookView(View):
    def post(self,request):
        if request.method == 'POST':
            form = IssuedBookForm(request.POST)
            if form.is_valid():
                #print(form.cleaned_data['isbn2'])
                #(form.cleaned_data['enrollment2'])
                #print(request.POST.get('isbn2'))
                #print(request.POST.get("enrollment2"))
                enrollement2 = request.POST.get('enrollment2')
                isbn2 =request.POST.get('isbn2')
               
                IssuedBook.objects.create(isbn=isbn2,enrollment=enrollement2)
        return render(request, 'library/book_issued.html')
    def get(self,request):
        form=IssuedBookForm()
        return render(request,"library/issue_book.html",{"form":form})



def issuedbook_view(request):
    issuedbooks=IssuedBook.objects.all()
    lis=[]
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>7:
            day=d-7
            fine=day*10

     
        books = list(Book.objects.filter(isbn=ib.isbn))
        students = list(StudentExtra.objects.filter(enrollment=ib.enrollment))
       
        i = 0
        for l in books:
            t = (students[i].get_name, students[i].enrollment,
                 books[i].name, books[i].author, issdate, expdate, fine)
            i = i+1
            lis.append(t)
        print(lis)
    return render(request,'library/view_issued_book.html',{'lis':lis})

def viewissuedbookbystudent(request):
    print(request.user.id)
    student=StudentExtra.objects.filter(user_id=request.user.id)
    
    issuedbook=IssuedBook.objects.filter(enrollment=student[0].enrollment)
     

    li1=[]

    li2=[]
    for ib in issuedbook:
        books=Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t=(request.user,student[0].enrollment,student[0].branch,book.name,book.author)
            li1.append(t)
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10
        t=(issdate,expdate,fine)
        li2.append(t)

    return render(request,'library/view_issued_book_by_student.html',{'li1':li1,'li2':li2})




class ContactusView(View):
    def post(self,request):
        if request.method=="POST":
            form=ContactusForm(request.POST)
            if form.is_valid():
                subject=form.cleaned_data['Subject']
                message=form.cleaned_data['Message']
                to=form.cleaned_data["Email"]
                sender="info.example.com"
                send_mail(subject, message, sender, [to,])
        return HttpResponse("Mail is sent to console")
    
    def get(self,request):
        form = form = ContactusForm()
        return render(request,"library/contactus.html",{'form':form})


class SearchBook(View):
    def post(self,request):
        if request.method=="POST":
            form=SearchForm(request.POST)
            if form.is_valid():
                book_name=form.cleaned_data['name']
                books=Book.objects.filter(name__icontains=book_name)
            return render(request,"library/search_result.html",{'books':books})
    
    def get(self,request):
        form=SearchForm()
        return render(request,"library/search_book_form.html",{"form":form})




class StudentSelfProfile(TemplateView):
    template_name="library/student_self_profile.html"

    def get_context_data(self,**kwargs):
        context= super().get_context_data(**kwargs)
        context['student']=User.objects.get(pk=kwargs['pk'])
        context['extra']=StudentExtra.objects.get(user_id=kwargs['pk'])
        print(context['extra'])
        return context
    
class AdminUpdateView(UpdateView):
    model=User
    fields = ['first_name', 'last_name', 'username','email']
    template_name="library/admin_update_form.html"
    success_url="/accounts/profile/"