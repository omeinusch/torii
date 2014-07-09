from datetime import datetime

from django.db import models
from django.db.models import permalink
from django.utils.text import slugify


class Phrases(object):
    def __getattr__(self, name):
        return (Phrase.objects.get_or_create(key=name)[0]).string


class Phrase(models.Model):
    key = models.SlugField(unique=True)
    string = models.TextField()

    def __unicode__(self):
        return self.string

    class Meta:
        verbose_name = 'Phrase'
        verbose_name_plural = 'Phrases'
        ordering = ['key']


class Configuration(models.Model):
    name = models.CharField(verbose_name='Name', max_length=30)
    url = models.URLField(verbose_name='URL Website')
    github_token = models.CharField(max_length=40)
    github_repository = models.CharField(max_length=100)
    github_development_branch = models.CharField(max_length=100)
    ohloh_project_url_name = models.CharField(max_length=100, blank=True)
    sourceforge_project_unixname = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Configuration'
        verbose_name_plural = 'Configurations'


class News(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    published = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey('auth.User', on_delete=models.PROTECT)

    @permalink
    def get_absolute_url(self):
        return 'news-detail', [str(self.slug)]

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(News, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ('-published', )
        get_latest_by = 'published'
