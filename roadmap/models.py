from __future__ import division
from django.db import models


class Label(models.Model):
    name = models.CharField(max_length=30, unique=True)
    color = models.CharField(max_length=6, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Label'
        verbose_name_plural = 'Labels'
        ordering = ['name']


class Milestone(models.Model):
    STATE_OPEN = 'open'
    STATE_CLOSED = 'closed'
    STATES = (
        (STATE_OPEN, 'Open'),
        (STATE_CLOSED, 'Closed')
    )
    guid = models.IntegerField(unique=True)  # id
    url = models.URLField(blank=True)
    state = models.CharField(max_length=6, choices=STATES, blank=True)
    title = models.CharField(max_length=140, blank=True)
    description = models.TextField(blank=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    closed = models.DateTimeField(blank=True, null=True)

    @property
    def progress(self):
        if self.total_issues == 0:
            return 0
        return int(self.closed_issues / self.total_issues * 100)

    @property
    def open_issues(self):
        return len(self.issue_set.filter(state=Issue.STATE_OPEN))

    @property
    def closed_issues(self):
        return len(self.issue_set.filter(state=Issue.STATE_CLOSED))

    @property
    def total_issues(self):
        return len(self.issue_set.all())

    @property
    def release(self):
        return Release.objects.get(tag_name=self.title)

    def issue_last_closed(self):
        try:
            return self.issue_set.filter(state=Issue.STATE_CLOSED).order_by('-closed')[0]
        except:
            return None

    def issue_first_created(self):
        try:
            return self.issue_set.filter(state=Issue.STATE_OPEN).order_by('created')[0]
        except:
            return None

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Milestone'
        verbose_name_plural = 'Milestones'
        ordering = ['-title']


class Issue(models.Model):
    STATE_OPEN = 'open'
    STATE_CLOSED = 'closed'
    STATES = (
        (STATE_OPEN, 'Open'),
        (STATE_CLOSED, 'Closed')
    )

    guid = models.IntegerField(unique=True)  # number
    url = models.URLField(blank=True)  # html_url
    state = models.CharField(max_length=6, choices=STATES, blank=True)
    title = models.CharField(max_length=140, blank=True)
    body = models.TextField(blank=True)
    milestone = models.ForeignKey(Milestone, null=True, blank=True)
    labels = models.ManyToManyField(Label, blank=True)
    created = models.DateTimeField(blank=True, null=True)
    updated = models.DateTimeField(blank=True, null=True)
    closed = models.DateTimeField(blank=True, null=True)

    @property
    def number(self):
        return self.guid

    def __unicode__(self):
        return '#{} {}'.format(self.guid, self.title)

    class Meta:
        verbose_name = 'Issue'
        verbose_name_plural = 'Issues'
        ordering = ['-state', '-guid']
        get_latest_by = 'created'


class Release(models.Model):
    guid = models.IntegerField(unique=True)  #id
    url = models.URLField(blank=True)  #html_url
    download_tar = models.URLField(blank=True)  #tarball_url
    download_zip = models.URLField(blank=True)  #zipball_url
    tag_name = models.CharField(max_length=20, blank=True)  #tag_name
    name = models.CharField(max_length=120, blank=True)  #name
    notes = models.TextField(blank=True)  #body
    stable = models.BooleanField(default=False)  #!prerelease
    published = models.DateTimeField(blank=True, null=True)  #published_at

    @property
    def milestone(self):
        return Milestone.objects.get(title=self.tag_name)

    def __unicode__(self):
        return self.name or self.tag_name

    class Meta:
        verbose_name = 'Release'
        verbose_name_plural = 'Releases'
        get_latest_by = 'published'
        ordering = ['-published']


class Commit(models.Model):
    sha = models.CharField(max_length=40)
    url = models.URLField(blank=True)
    committer_name = models.CharField(max_length=100, blank=True)
    committer_date = models.DateTimeField(blank=True, null=True)
    author_name = models.CharField(max_length=100, blank=True)
    author_date = models.DateTimeField(blank=True, null=True)
    message = models.TextField(blank=True)

    def __unicode__(self):
        return self.sha[:7]

    class Meta:
        verbose_name = 'Commit'
        verbose_name_plural = 'Commits'
        get_latest_by = 'committer_date'
        ordering = ['-committer_date']

