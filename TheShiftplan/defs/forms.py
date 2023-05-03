from django import forms
from django.forms.models import inlineformset_factory

from .models import Jobtype, Job, SubCrew
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput

# class RenewShiftplanForm(forms.Form):
#     new_name = forms.CharField(help_text="Enter a new name.")

class JobtypeForm(forms.ModelForm):
    class Meta:
        model = Jobtype
        fields = (
            'name',
            'description',
            'default_rating',
            'restricted_to_subcrew',
            'subcrew',
        )
    
    # def __init__(self, *args, **kwargs):
    #     super(JobtypeForm, self).__init__(*args, **kwargs)
    #     self.fields['subcrew'].queryset = Subcrew.objects.all()
    #     self.fields['subcrew'].widget.attrs['style'] = 'display:none'
    #     self.fields['subcrew'].widget.attrs['id'] = 'user_choice'
    #     self.fields['restricted_to_subcrew'].widget.attrs['onclick'] = "javascript:toggleDiv('user_choice');"


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = (
            'begin_date',
            'end_date',
            'begin_time',
            'end_time'
        )
        widgets = {
            'begin_date': DatePickerInput(),
            'end_date': DatePickerInput(),
            'begin_time': TimePickerInput(),
            'end_time': TimePickerInput(),
        }

JobtypeFormSet = inlineformset_factory(
    Jobtype,
    form=JobtypeForm,
    min_num=0,  # minimum number of forms that must be filled in
    extra=1,  # number of empty forms to display
    can_delete=True  # show a checkbox in each form to delete the row
)
