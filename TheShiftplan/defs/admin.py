from django.contrib import admin
import nested_admin
# from django.contrib.auth.admin import GroupAdmin
# from django.contrib.auth.models import User, Group
from .models import Jobtype, Job, SubCrew, UserProfile
from .forms import JobtypeForm

from .signals import *

class JobInline(nested_admin.NestedTabularInline):
    model = Job
    extra = 0

class JobtypeAdmin(nested_admin.NestedModelAdmin):
    model = Jobtype
    form = JobtypeForm
    fieldsets = [
        (None,               {'fields': ['name', 'description', 'default_rating', 'restricted_to_subcrew', 'subcrew']}),
    ]
    inlines = [JobInline,]
    extra = 0
    # That adds a “Filter” sidebar that lets people filter the change list by field:
    list_filter = ['name']
    # That adds a search box at the top of the change list.
    search_fields = ['name']




admin.site.register(Jobtype, JobtypeAdmin)

# class SubCrewAdmin(GroupAdmin):
#     model = SubCrew

admin.site.register(SubCrew)
admin.site.register(UserProfile)