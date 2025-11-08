from django.contrib import admin
from .models import Project, Review, Tag

# Register your models here.

# admin.site.register(Project)
# admin.site.register(Review)
admin.site.register(Tag)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('vote_total', 'vote_ratio')
    list_display = ('title', 'owner', 'vote_total', 'vote_ratio', 'created')
    search_fields = ('title', 'owner__username')
    
    # filter by tags and owner
    list_filter = ('tags', 'owner')

        
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_filter = ('value', 'project')
    list_display = ('project', 'owner', 'value', 'created')

    # whenever a review is saved via admin, update the associated project's vote counts
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request=request, obj=obj, form=form, change=change)  # call the real save() method
    #     obj.project.getVoteCount   # update vote count for the associated project
    #     obj.project.save()         # save updated vote count to DB

    # whenever a review is deleted via admin, update the associated project's vote counts
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        obj.project.getVoteCount
        obj.project.save()

    

