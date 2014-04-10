from django.contrib import admin
from models import Configuration, Phrase, News


class ConfigurationAdmin(admin.ModelAdmin):
    pass


class PhraseAdmin(admin.ModelAdmin):
    list_display = ('key', 'string')


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'published')
    list_filter = ('user', 'published')


admin.site.register(Configuration, ConfigurationAdmin)
admin.site.register(Phrase, PhraseAdmin)
admin.site.register(News, NewsAdmin)
