from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Review


# update project vote counts on every review save
@receiver(post_save, sender=Review)
def update_project_vote_count(sender, instance, created, **kwargs):
    instance.project.getVoteCount  # update vote count for the associated project
    instance.project.save()        # save updated vote count to DB