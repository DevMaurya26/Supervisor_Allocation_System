from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    COLLEGE = [
        ('SCET','SCET'),
        ('DDU','DDU'),
        ('XYZ','XYZ'),
        ('NIT','NIT'),
    ]

    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.ChoiceField(choices=COLLEGE,label='select college', widget=forms.Select)
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']