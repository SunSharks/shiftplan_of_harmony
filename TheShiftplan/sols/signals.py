from .models import SolutionRun, Solution, UserJobAssignment

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Solution)
def solution_run_saved(sender, instance, created, **kwargs):
    if instance.final:
        final_sol_objs = Solution.objects.filter(final=True, solution_run=instance.solution_run)
        print(final_sol_objs)
        if len(final_sol_objs) > 0:
            for f in final_sol_objs:
                f.final = False
                f.save()
            setattr(instance, final, True)
            instance.save()



        # jobs = Job.objects.all()
        # for j in jobs:
        #     UserJobRating.objects.create(user=instance, job=j, rating=j.rating)