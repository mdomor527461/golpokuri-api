from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.StoryReact)
@admin.register(models.Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'read_count')
    filter_horizontal = ('reader',)  # This adds a nice UI to manage many-to-many


admin.site.register(models.Comment)
admin.site.register(models.CommentReaction)
admin.site.register(models.StoryRating)