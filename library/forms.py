from django import forms
from django.contrib.auth.models import User
from . import models

class SearchForm(forms.Form):
    name=forms.CharField(max_length=30,label="Enter Book Name")


class ContactusForm(forms.Form):
    Subject = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(
        max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class AdminSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
       
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','password']


class StudentUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        
        model = User
        fields = ['first_name', 'last_name', 'username','email', 'password']


class StudentExtraForm(forms.ModelForm):
    class Meta:
        model = models.StudentExtra
        fields = ['enrollment', 'branch']


class BookForm(forms.ModelForm):
    class Meta:
        model = models.Book
        fields = ['name', 'isbn', 'author', 'category']


class IssuedBookForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of book model will be shown there in html
    isbn2 = forms.ModelChoiceField(queryset=models.Book.objects.all(
    ), empty_label="Name and isbn", to_field_name="isbn", label='Name and Isbn')
    enrollment2 = forms.ModelChoiceField(queryset=models.StudentExtra.objects.all(
    ), empty_label="Name and enrollment", to_field_name='enrollment', label='Name and enrollment')



