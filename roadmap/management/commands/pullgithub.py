from django.core.management import BaseCommand
import requests

from content.models import Configuration
from roadmap.models import Release, Label, Milestone, Issue, Commit


class Command(BaseCommand):
    args = ''
    help = 'Synchronizes the github project.'

    conf = Configuration.objects.first()
    github_repository = conf.github_repository  # like 'omeinusch/torii'
    github_token = conf.github_token  # like sha1

    server = 'https://api.github.com'

    format_dict = {'server': server, 'repository': github_repository}

    path_releases = '{server}/repos/{repository}/releases'.format(**format_dict)
    path_labels = '{server}/repos/{repository}/labels'.format(**format_dict)
    path_milestones = '{server}/repos/{repository}/milestones'.format(**format_dict)
    path_issues = '{server}/repos/{repository}/issues'.format(**format_dict)
    path_development_branch = '{server}/repos/{repository}/git/refs/heads/{development_branch}'.format(
        development_branch=conf.github_development_branch, **format_dict)

    headers_dict = {'Authorization': 'token {0}'.format(github_token)}

    def handle(self, *args, **options):
        self._pull_releases()
        self._pull_labels()
        self._pull_milestones()
        self._pull_issues()
        self._pull_development()

    def _iterate_requests(self, url, params, method):
        r = requests.get(url, headers=self.headers_dict, params=params)
        for thing in r.json():
            method(thing)
        if 'link' in r.headers:
            if 'next' in r.links:
                self._iterate_requests(r.links['next']['url'], params, method)

    def _pull_releases(self):
        self._iterate_requests(self.path_releases, {}, self._handle_release)

    def _pull_labels(self):
        self._iterate_requests(self.path_labels, {}, self._handle_label)

    def _pull_issues(self):
        self._iterate_requests(self.path_issues, {'state': 'all'}, self._handle_issue)

    def _pull_milestones(self):
        self._iterate_requests(self.path_milestones, {'state': 'closed'}, self._handle_milestone)
        self._iterate_requests(self.path_milestones, {'state': 'open'}, self._handle_milestone)

    def _pull_development(self):
        r = requests.get(self.path_development_branch, headers=self.headers_dict)
        r = requests.get(r.json()['object']['url'])
        commit_set = r.json()
        commit = Commit.objects.get_or_create(sha=commit_set['sha'])[0]
        commit.url = commit_set['html_url']
        commit.committer_name = commit_set['committer']['name']
        commit.committer_date = commit_set['committer']['date']
        commit.author_name = commit_set['author']['name']
        commit.author_date = commit_set['author']['date']
        commit.message = commit_set['message']
        commit.save()

    @staticmethod
    def _handle_development(development_set):
        print development_set

    @staticmethod
    def _handle_release(release_set):
        release = Release.objects.get_or_create(guid=release_set['id'])[0]
        release.url = release_set['html_url']
        release.download_tar = release_set['tarball_url']
        release.download_zip = release_set['zipball_url']
        release.tag_name = release_set['tag_name']
        release.name = release_set['name']
        release.notes = release_set['body']
        release.stable = not release_set['prerelease']
        release.published = release_set['published_at']
        release.save()

    @staticmethod
    def _handle_label(label_set):
        label = Label.objects.get_or_create(name=label_set['name'])[0]
        label.color = label_set['color']
        label.save()

    @staticmethod
    def _handle_milestone(milestone_set):
        milestone = Milestone.objects.get_or_create(guid=milestone_set['id'])[0]
        milestone.url = milestone_set['url']
        milestone.state = milestone_set['state']
        milestone.title = milestone_set['title']
        milestone.description = milestone_set['description']
        milestone.created = milestone_set['created_at']
        milestone.updated = milestone_set['updated_at']
        milestone.closed = milestone_set['due_on']
        milestone.save()

    @staticmethod
    def _handle_issue(issue_set):
        issue = Issue.objects.get_or_create(guid=issue_set['number'])[0]
        issue.url = issue_set['html_url']
        issue.state = issue_set['state']
        issue.title = issue_set['title']
        issue.body = issue_set['body']
        if issue_set['milestone']:
            issue.milestone = Milestone.objects.get(guid=issue_set['milestone']['id'])
        if issue_set['labels']:
            label_set = []
            for label in issue_set['labels']:
                label_set.append(Label.objects.get(name=label['name']))
            issue.labels = label_set
        issue.created = issue_set['created_at']
        issue.updated = issue_set['updated_at']
        issue.closed = issue_set['closed_at']
        issue.save()
