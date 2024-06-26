from django.contrib import admin
from .models import *
class Profile_list(admin.ModelAdmin):
    list_display=['id','user','id_user','bio','profileimg','location']

admin.site.register(Profile,Profile_list)
admin.site.register(Post)
admin.site.register(LikePost)
admin.site.register(followercount)
