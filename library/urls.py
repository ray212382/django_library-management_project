from django.urls import path

from django.contrib.auth import views as auth_views
from .import views
from library.views import  AdminUpdateView,StudentSelfProfile,SearchBook, IssueBookView,ListStudentView,ContactusView,ListBookView ,CreateBookView,AdminSignupView,HomeTemplateView,ProfileTemplateView,StudentSignupView,TemplateBookAddedView

app_name="library"
urlpatterns=[
    path("", HomeTemplateView.as_view(),name="home" ),
    path("adminsignup/",AdminSignupView.as_view(), name='adminsignup'),
    path("studentsignup/",StudentSignupView.as_view(), name='studentsignup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path("login/", auth_views.LoginView.as_view(template_name="library/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='library/index.html'),name="logout"),
    path('accounts/profile/', views.postlogin_view, name="postlogin"),
    path('addbook/',CreateBookView.as_view(),name="addbook"),
    path("bookadded/",TemplateBookAddedView.as_view(),name="bookadded" ),
    path("bookview/", ListBookView.as_view(), name="listbookview"),
    path("studentview/",ListStudentView.as_view(),),
    path("issuebookview/", IssueBookView.as_view(),name="issuebookview"),
    path("issuedbookview/",views.issuedbook_view,name="issuedbookview"),
    path("viewissuedbookbystudent/", views.viewissuedbookbystudent,
         name="viewissuedbookbystudent"),
    path("adminprofile/<int:pk>/",AdminUpdateView.as_view(), name="adminprofile"),
    
    path("studentprofile/<int:pk>/", StudentSelfProfile.as_view(), name="studentprofile"),
    path("searchbook/",SearchBook.as_view(),name="searchbook"),
    path("contactus/", ContactusView.as_view(), name="contactus"),
    
]