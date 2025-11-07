from django.contrib import admin
from .models import Profile, Skill


# Register your models here.
# admin.site.register(Profile)
admin.site.register(Skill)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'username', 'location']


admin.site.register(Profile, ProfileAdmin)