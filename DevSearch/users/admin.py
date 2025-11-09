from django.contrib import admin
from .models import Profile, Skill, Message


# Register your models here.
# admin.site.register(Profile)
admin.site.register(Skill)

@admin.register(Profile)    # using decorator to register model with admin site
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'username', 'location']


# admin.site.register(Profile, ProfileAdmin)    # not needed if decorator is used 

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'sender', 'recipient', 'is_read', 'created']
    