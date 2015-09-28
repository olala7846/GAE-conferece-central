#!/usr/bin/env python

"""models.py

Udacity conference server-side Python App Engine data & ProtoRPC models

$Id: models.py,v 1.1 2014/05/24 22:01:10 wesc Exp $

created/forked from conferences.py by wesc on 2014 may 24

"""

import httplib
import endpoints
from protorpc import messages
from google.appengine.ext import ndb


class ConflictException(endpoints.ServiceException):
    """ConflictException -- exception mapped to HTTP 409 response"""
    http_status = httplib.CONFLICT


class Profile(ndb.Model):
    """Profile -- User profile object"""
    displayName = ndb.StringProperty()
    mainEmail = ndb.StringProperty()
    teeShirtSize = ndb.StringProperty(default='NOT_SPECIFIED')
    conferenceKeysToAttend = ndb.StringProperty(repeated=True)
    sessionWishList = ndb.StringProperty(repeated=True)


# protorpc classes

class ProfileMiniForm(messages.Message):
    """ProfileMiniForm -- update Profile form message"""
    displayName = messages.StringField(1)
    teeShirtSize = messages.EnumField('TeeShirtSize', 2)


class ProfileForm(messages.Message):
    """ProfileForm -- Profile outbound form message"""
    displayName = messages.StringField(1)
    mainEmail = messages.StringField(2)
    teeShirtSize = messages.EnumField('TeeShirtSize', 3)
    conferenceKeysToAttend = messages.StringField(4, repeated=True)


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    data = messages.StringField(1, required=True)


class BooleanMessage(messages.Message):
    """BooleanMessage-- outbound Boolean value message"""
    data = messages.BooleanField(1)


class Conference(ndb.Model):
    """Conference -- Conference object"""
    name = ndb.StringProperty(required=True)
    description = ndb.StringProperty()
    organizerUserId = ndb.StringProperty()
    topics = ndb.StringProperty(repeated=True)
    city = ndb.StringProperty()
    startDate = ndb.DateProperty()
    month = ndb.IntegerProperty()
    endDate = ndb.DateProperty()
    maxAttendees = ndb.IntegerProperty()
    seatsAvailable = ndb.IntegerProperty()


class ConferenceForm(messages.Message):
    """ConferenceForm -- Conference outbound form message"""
    name = messages.StringField(1)
    description = messages.StringField(2)
    organizerUserId = messages.StringField(3)
    topics = messages.StringField(4, repeated=True)
    city = messages.StringField(5)
    startDate = messages.StringField(6)  # DateTimeField()
    month = messages.IntegerField(7)
    maxAttendees = messages.IntegerField(8)
    seatsAvailable = messages.IntegerField(9)
    endDate = messages.StringField(10)  # DateTimeField()
    websafeKey = messages.StringField(11)  # ndb conference id in websafe form
    organizerDisplayName = messages.StringField(12)


class ConferenceForms(messages.Message):
    """ConferenceForms -- multiple Conference outbound form message"""
    items = messages.MessageField(ConferenceForm, 1, repeated=True)


class TeeShirtSize(messages.Enum):
    """TeeShirtSize -- t-shirt size enumeration value"""
    NOT_SPECIFIED = 1
    XS_M = 2
    XS_W = 3
    S_M = 4
    S_W = 5
    M_M = 6
    M_W = 7
    L_M = 8
    L_W = 9
    XL_M = 10
    XL_W = 11
    XXL_M = 12
    XXL_W = 13
    XXXL_M = 14
    XXXL_W = 15


class ConferenceQueryForm(messages.Message):
    """ConferenceQueryForm -- Conference query inbound form message"""
    field = messages.StringField(1)
    operator = messages.StringField(2)
    value = messages.StringField(3)


class ConferenceQueryForms(messages.Message):
    """
    ConferenceQueryForms -- multiple ConferenceQueryForm inbound form message
    """
    filters = messages.MessageField(ConferenceQueryForm, 1, repeated=True)


class Session(ndb.Model):
    """
    Session -- session in a conference
    Should have parent/child relationship with Conference
    """
    name = ndb.StringProperty(required=True)
    highlights = ndb.TextProperty()
    speakerName = ndb.StringProperty()
    duration = ndb.IntegerProperty()  # duration in minutes
    sessionType = ndb.StringProperty(default='NOT_SPECIFIED')
    date = ndb.DateProperty()
    startTime = ndb.TimeProperty()


class SessionForm(messages.Message):
    """SessionForm -- Session outbound form message"""
    name = messages.StringField(1, required=True)
    highlights = messages.StringField(2)
    speakerName = messages.StringField(3)
    duration = messages.IntegerField(4)
    sessionType = messages.EnumField('SessionType', 5)
    date = messages.StringField(6)  # DateProperty()
    startTime = messages.StringField(7)  # TimeProperty()
    websafeKey = messages.StringField(8)  # ndb conference id in websafe form


class SessionType(messages.Enum):
    """SessionType -- session type in conference"""
    NOT_SPECIFIED = 1
    KEY_NOTE = 2
    LECTURE = 3
    WORKSHOP = 4


class SessionForms(messages.Message):
    """
    SessionForms -- multiple SessionForm inbound for sessions
    """
    items = messages.MessageField(SessionForm, 1, repeated=True)


class SessionTypeForm(messages.Message):
    """SessionTypeForm -- query session by type"""
    sessionType = messages.EnumField('SessionType', 1)


class SessionSpeakerForm(messages.Message):
    """SessionSpeakerForm -- query session by speakerName"""
    speakerName = messages.StringField(1)


class UpcomingConferencesForm(messages.Message):
    """UpcomingConferencesForm -- query all upcoming conferences"""
    count = messages.IntegerField(1)  # number of conferences to return


class ProfileForms(messages.Message):
    """ProfileForms -- list of Profile objects"""
    items = messages.MessageField(ProfileForm, 1, repeated=True)
