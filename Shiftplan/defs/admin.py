from django.contrib import admin
import nested_admin
from .models import Shiftplan
# from .models import Subgroup
# from .models import Day
from .models import Jobtype
from .models import Job


class JobInline(nested_admin.NestedStackedInline):
    model = Job
    extra = 3

class JobtypeInline(nested_admin.NestedStackedInline):
    model = Jobtype
    inlines = [JobInline]


class ShiftplanAdmin(nested_admin.NestedModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'group']}),
    ]
    inlines = [JobtypeInline,]
    # list_display = ('name', 'group')
    # That adds a “Filter” sidebar that lets people filter the change list by field:
    list_filter = ['name']
    # That adds a search box at the top of the change list.
    search_fields = ['name']


admin.site.register(Shiftplan, ShiftplanAdmin)
