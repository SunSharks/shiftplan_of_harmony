from django.contrib import admin

from .models import Shiftplan
# from .models import Subgroup
# from .models import Day
from .models import Jobtype
from .models import Job


# class SubgroupInline(admin.StackedInline):
#     model = Subgroup
#     extra = 1


class ShiftplanAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'group']}),
    ]
    # inlines = [SubgroupInline]


admin.site.register(Shiftplan, ShiftplanAdmin)
# admin.site.register(Day)
admin.site.register(Jobtype)
admin.site.register(Job)
# admin.site.register(Subgroup)
