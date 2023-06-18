import logging

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q

from .models import UserCandidate


class RegisterForm(UserCreationForm):
    username = forms.CharField(max_length = 100)
    email  = forms.EmailField(max_length = 100, required=False)
    password1 = forms.CharField(widget = forms.PasswordInput(), max_length = 100)
    password2 = forms.CharField(widget = forms.PasswordInput(),  max_length = 100)
    first = forms.CharField(max_length = 100, required=False)
    last = forms.CharField(max_length = 100, required=False)

    class Meta:
        model = User
        fields = ['username', 'first', 'last', 'email','password1','password2']


    def find_user_candidate(self):
        whole_name = {
            "forename": self.cleaned_data.get("first"),
            "surname": self.cleaned_data.get("last")
        }
        email = {
            "email": self.cleaned_data.get("email")
        }
        
        contains_none_vals = lambda data: True if None in data.values() else False
        rm_none_vals = lambda data: {key: val for key, val in data.items() if not val is None}
        # whole_name = rm_none_vals(whole_name)
        email = rm_none_vals(email)
        data = whole_name.update(email)

        user_cand = UserCandidate.objects.filter(**data)
        logging.debug(user_cand)
        if len(user_cand) == 0 and not contains_none_vals(whole_name):
            user_cand = UserCandidate.objects.filter(**whole_name)
            logging.debug(user_cand)
        if len(user_cand) == 0 and len(email) > 0:
            user_cand = UserCandidate.objects.filter(**email)
            logging.debug(user_cand)
        if len(user_cand) == 0:
            raise forms.ValidationError(f"No existing UserCandidate found for {data}")
        if len(user_cand) > 1:
            raise forms.ValidationError(f"Multiple UserCandidate found for {data}")
        user_cand = user_cand[0]
        logging.debug(user_cand)
        if not user_cand.user is None:
            raise forms.ValidationError(f"You already have an account.")
        else:
            username = self.cleaned_data.get("username")
            if not username : 
                username = user_cand.forename + " " + user_cand.surname
                logging.debug(self.username)
            try : 
                user = User.objects.get(username = username)
            except :
                user = None
            if user : 
                raise forms.ValidationError("User with the username -: {} already exits ".format(username))
            return username