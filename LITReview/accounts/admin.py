from django.contrib import admin
from .models import Ticket, Review, UserFollows

"""class UserFollowAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user")
    """


class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "description", "time_created")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("headline", "time_created")


class UserFollowsadmin(admin.ModelAdmin):
    list_display = ("user", "followed_user")

# Register your models here.


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserFollows, UserFollowsadmin)
