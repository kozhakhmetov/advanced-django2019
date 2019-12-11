from django.contrib import admin

# Register your models here.
from core.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    pass
    # list_display = ('id', 'name', 'creator_name', 'creator_id', )

