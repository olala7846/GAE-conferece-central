#!/usr/bin/env python

"""
main.py -- Udacity conference server-side Python App Engine
    HTTP controller handlers for memcache & task queue access

$Id$

created by wesc on 2014 may 24

"""

import webapp2
from google.appengine.api import app_identity
from google.appengine.api import mail
from conference import ConferenceApi
from models import Profile, Conference, Session


class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)


class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )


class MockConferenceData(webapp2.RequestHandler):
    def get(self):
        """Mock objects for testing"""
        ConferenceApi._mockConferenceData()
        self.response.set_status(200)
        self.response.write('Mock Success')


class CheckForFeaturedSpeaker(webapp2.RequestHandler):
    def post(self):
        """
        Check if there is more than one session by a speaker single conference
        """
        wssk = self.request.get('websafeSessionKey')
        ConferenceApi._checkForFeaturedSpeaker(wssk)


app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/check_featured_speaker', CheckForFeaturedSpeaker),
    ('/mock/mock_conference_data', MockConferenceData),
], debug=True)
