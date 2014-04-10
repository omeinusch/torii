from django.contrib import admin
from roadmap.models import Label, Milestone, Issue, Release, Commit


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'tag_name', 'stable', 'published')
    list_filter = ('stable', 'published')


class LabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')


class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'state', 'created', 'updated', 'closed')
    list_filter = ('state', 'created', 'updated', 'closed')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('guid', 'title', 'state', 'milestone', 'created', 'updated', 'closed')
    list_filter = ('state', 'milestone', 'created', 'updated', 'closed')
    list_display_links = ('title', )


class CommitAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'committer_name', 'committer_date', 'author_name', 'author_date')
    list_filter = ('committer_name', 'committer_date', 'author_name', 'author_date')


admin.site.register(Label, LabelAdmin)
admin.site.register(Milestone, MilestoneAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Release, ReleaseAdmin)
admin.site.register(Commit, CommitAdmin)
