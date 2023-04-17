from django import forms
from django.forms.models import inlineformset_factory

from .models import UserOptions
# from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

# class RenewShiftplanForm(forms.Form):
#     new_name = forms.CharField(help_text="Enter a new name.")



class UserOptionsForm(forms.ModelForm):
    class Meta:
        model = UserOptions
        fields = (
            'min_break_hours',
        )
        widgets = {
        }
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserOptionsForm, self).__init__(*args, **kwargs)


