from django.contrib import admin
import nested_admin
from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import User, Group
from .models import Shiftplan
from .models import ShiftplanCrew
from .models import ShiftplanCrewMember
from .models import Jobtype
from .models import Job
# from .models import SubCrew


class JobInline(nested_admin.NestedTabularInline):
    model = Job
    extra = 0

class JobtypeInline(nested_admin.NestedStackedInline):
    model = Jobtype
    inlines = [JobInline]
    extra = 0

# class SubCrewInline(nested_admin.NestedStackedInline):
#     model = SubCrew
#     extra = 0


class ShiftplanAdmin(nested_admin.NestedModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'group']}),
    ]
    # inlines = [JobtypeInline, SubCrewInline,]
    inlines = [JobtypeInline,]
    # list_display = ('name', 'group')
    # That adds a “Filter” sidebar that lets people filter the change list by field:
    list_filter = ['name']
    # That adds a search box at the top of the change list.
    search_fields = ['name']


admin.site.register(Shiftplan, ShiftplanAdmin)

class ShiftplanCrewMemberInline(admin.StackedInline):
    model = ShiftplanCrewMember
    extra = 1

class ShiftplanCrewAdmin(GroupAdmin):
    model = ShiftplanCrew
    inlines = [ShiftplanCrewMemberInline]
    filter_horizontal = ('members',)

admin.site.unregister(Group)
admin.site.register(ShiftplanCrew, ShiftplanCrewAdmin)