# -*- coding: utf-8 -*-
"""
    sentry_campfire.plugin
    ~~~~~~~~~~~~~~~~~~~~~~

    This module enables Campfire notifications from Sentry
    
    :copyright: (c) 2012 Mustafa Khattab
    :license: BSD    
"""
from camplight import Request, Campfire
from django import forms

from sentry.conf import settings
from sentry.plugins import Plugin

import sentry_campfire


class CampfireOptionsForm(forms.Form):
    url = forms.URLField(required=True,
                          label='Campfire URL',
                          help_text='e.g. https://your-subdomain.campfirenow.com')
    token = forms.CharField(required=True,
                            label='API Token')
    rooms = forms.CharField(required=True,
                            help_text='Rooms to send notifications to, separated by comma')
    sound = forms.CharField(initial='rimshot',
                            help_text='Sound to play (e.g. rimshot, greatjob, tada, etc.). Defaults to rimshot.')
    play_sound = forms.BooleanField(required=False)


class CampfireNotification(Plugin):
    title = 'Campfire'
    slug = 'campfire'
    description = 'Send Campfire notifications'
    version = sentry_campfire.VERSION
    author = 'Mustafa Khattab'
    author_url = 'https://github.com/mkhattab/sentry-campfire'
    resource_links = [
    ('Bug Tracker', 'https://github.com/mkhattab/sentry-campfire/issues'),
    ('Source', 'https://github.com/mkhattab/sentry-campfire'),
    ]
    
    project_conf_form = CampfireOptionsForm

    
    def is_configured(self, project, **kwargs):        
        return all(self.get_option(k, project) for k in ('url', 'token', 'rooms'))

    def post_process(self, group, event, is_new, is_sample, **kwargs):
        if not is_new or not self.is_configured(event.project):
            return
        
        link = '%s/%s/group/%d/' % (settings.URL_PREFIX, group.project.slug,
                                    group.id)
        message = '[%s] %s (%s)' % (event.server_name, event.message, link)

        self.send_notification(event.project, message)

    def send_notification(self, project, message):
        url = self.get_option('url', project)
        token = self.get_option('token', project)
        rooms = self.get_option('rooms', project)
        play_sound = self.get_option('play_sound', project)
        sound = self.get_option('sound', project)

        req = Request(url.strip('/'), token) # The appended slash causes a 404 error
        campfire = Campfire(req)
        
        for r in rooms.split(','):
            if r:
                room = campfire.room(r)
                room.speak(message)
                if play_sound:
                    room.play(sound)
                    
