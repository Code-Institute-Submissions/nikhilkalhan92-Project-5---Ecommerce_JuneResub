from tokenize import Comment
from django import forms
from django.forms import ModelForm

from django.contrib.auth.models import User               #for costimizig  user,registeration form
from django.contrib.auth.forms import UserCreationForm          #used for login and register
from .models import Comments


#html mai hr form k andar csrf_token add krna huga form k andar wrna error aeyga
class taskform(forms.ModelForm):
    title=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Write comment....'})) # setting a placeholder in our form

    class Meta:     # we need to give at leasts two values

        model=Comments   # jis model keliye form banana hai wo, aur kiti fields rkhni hai form mai
        fields='__all__' 