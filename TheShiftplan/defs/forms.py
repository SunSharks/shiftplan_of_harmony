from django import forms
from django.forms.models import inlineformset_factory
from django.forms.widgets import SelectMultiple
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

from .models import Jobtype, Job, SubCrew
from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput


# class RenewShiftplanForm(forms.Form):
#     new_name = forms.CharField(help_text="Enter a new name.")

class JobtypeForm(forms.ModelForm):
    class Meta:
        model = Jobtype
        fields = '__all__'

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if not self.instance.restricted_to_subcrew:
    #         self.fields['subcrew'].widget = forms.HiddenInput()
    
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

    def clean(self):
        cleaned_data = super().clean()
        begin_date = cleaned_data.get("begin_date")
        end_date = cleaned_data.get("end_date")
        begin_time = cleaned_data.get("begin_time")
        end_time = cleaned_data.get("end_time")

        if begin_time >= end_time:
            if begin_date >= end_date:
                raise ValidationError(
                    "Begin has to be before end."
                )
        if begin_date > end_date:
                raise ValidationError(
                    "Begin date has to be before end date."
                )

# JobtypeFormSet = inlineformset_factory(
#     model=Jobtype,
#     form=JobtypeForm,
#     min_num=0,  # minimum number of forms that must be filled in
#     extra=1,  # number of empty forms to display
#     can_delete=True  # show a checkbox in each form to delete the row
# )

class SubCrewForm(forms.ModelForm):
    class Meta:
        model = SubCrew
        fields = '__all__'
        # print(SubCrew.objects.filter())
        print("")
        members = forms.ModelMultipleChoiceField(
            queryset=User.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )
        # widgets = {
        #     # 'members': forms.CheckboxSelectMultiple(initial=initial_values),
        #     'members': forms.CheckboxSelectMultiple(),
        # }

    def __init__(self, *args, **kwargs):
        super(SubCrewForm, self).__init__(*args, **kwargs)
        try:
            us = [(m.id, m) for m in User.objects.all()]
            subcrew_members = kwargs["instance"].members.all()
            members = [m.id for m in subcrew_members]
            self.fields['members'] = forms.MultipleChoiceField(
                label=kwargs["instance"].name,
                initial=members,
                widget=forms.CheckboxSelectMultiple,
                choices=us
            )
            print(self.initial["members"])
        except:
            print("no preselected members.")
            us = [(m.id, m) for m in User.objects.all()]
            self.fields['members'] = forms.MultipleChoiceField(
                label="Members",
                initial=[],
                widget=forms.CheckboxSelectMultiple,
                choices=us
            )
        
        
        # members =  User.objects.filter()
        # self.fields['members'] =  forms.CheckboxSelectMultiple(initial=initial_values)
        

    # def current_members_labels(self):
    #     return [label for value, label in self.fields['genders'].choices if value in self['genders'].value()]

    # members = forms.ModelMultipleChoiceField(
    #     queryset=Member.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )

# from defs.forms import SubCrewForm; f = SubCrewForm(initial={'members': ['male', 'female']}); print f.selected_genders_labels()