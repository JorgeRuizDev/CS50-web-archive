from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.Comment)
admin.site.register(models.Post)
admin.site.register(models.Test)

class your_model_admin(admin.ModelAdmin):
    filter_horizontal = 'user'