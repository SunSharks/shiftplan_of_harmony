from django import forms
from django.forms.models import inlineformset_factory

from .models import UserOptions, BiasHours
# from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

# class RenewShiftplanForm(forms.Form):
#     new_name = forms.CharField(help_text="Enter a new name.")



class UserOptionsForm(forms.ModelForm):
    class Meta:
        model = UserOptions
        fields = (
            'min_break_hours',
            # 'bias_hours',
            # 'bias_hours_explanation',
        )


class BiasHoursForm(forms.ModelForm):
    class Meta:
        model = BiasHours
        fields = (
            'bias_hours',
            'explanation',
        )