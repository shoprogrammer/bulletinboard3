from django import forms
from .models import BoardModel,CommentModel,FavoriteModel,ReactionModel,Contact,LikeModel
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView

class BoardForm(forms.ModelForm):
    class Meta:
        model = BoardModel
        fields = ['title','content','image']


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ['content','image']


class ReactionForm(forms.ModelForm):
    class Meta:
        model = ReactionModel
        fields = ['content','image']
        






class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,help_text="emailアドレスは必須です")

    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class LikeForm(forms.ModelForm):
    class Meta:
        model = LikeModel
        fields = ['board']






class FavoriteForm(forms.ModelForm):

    class Meta:
        model = FavoriteModel
        fields = ['board']

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields =['title','message','email']