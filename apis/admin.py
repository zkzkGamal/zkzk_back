from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Tags)
admin.site.register(models.ProjectPost)
admin.site.register(models.post_comment)
admin.site.register(models.notify_user)
