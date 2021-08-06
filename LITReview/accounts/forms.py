from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Ticket, Review, UserFollows


class CreateAnUser(forms.Form):

    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"})
                               )
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"})
                               )
    repeatedpassword = forms.CharField(required=True,
                                       widget=forms.PasswordInput(attrs={"placeholder": "Confirmer mot de passe"})
                                       )

    def clean_username(self):
        data = self.cleaned_data.get("username")
        if User.objects.filter(username=data).exists() :
            raise forms.ValidationError("nom d'utilisateur impossible")
        return data

    def clean(self):
        repeatedpassword = self.cleaned_data.get('repeatedpassword')
        password = self.cleaned_data.get('password')
        if not password == repeatedpassword:
            raise forms.ValidationError('mot de passe non identique')
        return self.cleaned_data


class CreateATicket(ModelForm):

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class CreateAReview(ModelForm):
    CHOICES = [(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    rating = forms.ChoiceField(required=True,
                               widget=forms.RadioSelect, choices=CHOICES)

    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']


class CreateAUserFollow(ModelForm):
    class Meta:
        model = UserFollows
        fields = ["user", "followed_user"]


class FollowAUser(forms.Form):

    following = forms.CharField(required=True,
                                widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur"})
                                )

    def clean_following(self):
        data = self.cleaned_data.get("following")
        if not User.objects.filter(username=data).exists():
            raise forms.ValidationError("cet utilisateur n'existe pas")
        return data

    def existing(self, userconnected):
        try:
            utilisateur = User.objects.get(username=self.cleaned_data.get("following"))
            UserFollows.objects.get(user=userconnected,
                                    followed_user=utilisateur)
            return True
        finally:
            return False
