from django import forms
from django.forms.models import inlineformset_factory

from .models import Shiftplan, Jobtype, Job, TimeInterval


# class RenewShiftplanForm(forms.Form):
#     new_name = forms.CharField(help_text="Enter a new name.")

class TimeIntervalForm(forms.ModelForm):
    class Meta:
        model = TimeInterval
        fields = (
            'start_date',
            'end_date'
        )


class JobtypeForm(forms.ModelForm):
    class Meta:
        model = Jobtype
        fields = (
            'name',
            'description'
        )


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = (
            'begin',
            'end'
        )


TimeFormSet = inlineformset_factory(
    Shiftplan,
    TimeInterval,
    form=TimeIntervalForm,
    min_num=0,  # minimum number of forms that must be filled in
    extra=1,  # number of empty forms to display
    can_delete=True  # show a checkbox in each form to delete the row
)

JobtypeFormSet = inlineformset_factory(
    Shiftplan,
    Jobtype,
    form=JobtypeForm,
    min_num=0,  # minimum number of forms that must be filled in
    extra=1,  # number of empty forms to display
    can_delete=True  # show a checkbox in each form to delete the row
)
