import json
import os
import time
import uuid

import endpoints

from google.appengine.api import urlfetch
from google.appengine.ext import ndb
from models import Profile


def getUserId(user, id_type="email"):
    if id_type == "email":
        return user.email()

    if id_type == "oauth":
        """A workaround implementation for getting userid."""
        auth = os.getenv('HTTP_AUTHORIZATION')
        bearer, token = auth.split()
        token_type = 'id_token'
        if 'OAUTH_USER_ID' in os.environ:
            token_type = 'access_token'
        url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?%s=%s'
               % (token_type, token))
        user = {}
        wait = 1
        for i in range(3):
            resp = urlfetch.fetch(url)
            if resp.status_code == 200:
                user = json.loads(resp.content)
                break
            elif resp.status_code == 400 and 'invalid_token' in resp.content:
                url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?%s=%s'
                       % ('access_token', token))
            else:
                time.sleep(wait)
                wait = wait + i
        return user.get('user_id', '')

    if id_type == "custom":
        # implement your own user_id creation and getting algorythm
        # this is just a sample that queries datastore for an existing profile
        # and generates an id if profile does not exist for an email
        profile = Conference.query(Conference.mainEmail == user.email())
        if profile:
            return profile.id()
        else:
            return str(uuid.uuid1().get_hex())


def getConferenceFromRequest(request):
    """
    Validates and gets conference by 'websafeConferenceKey' inside request
    throws NotFoundException if no such conference in database
    """
    wsck = getattr(request, 'websafeConferenceKey')
    if not wsck:
        raise endpoints.NotFoundException('No conference key provided')

    conf = ndb.Key(urlsafe=wsck).get()
    if not conf:
        raise endpoints.NotFoundException(
            'No conference found with key: %s' % wsck)

    if not isinstance((session, 'Conference')):
        raise endpoints.NotFoundException('No Conference Found With Key')

    return conf


def getSessionFromRequest(request):
    """
    Validates and gets session by 'websafeSessionKey' in request
    Throws NotFoundException
    """
    wssk = getattr(request, 'websafeSessionKey')
    if not wssk:
        raise endpoints.NotFoundException('No session key provided')

    session = ndb.Key(urlsafe=wssk).get()
    if not session:
        raise endpoints.NotFoundException(
            'No conference foud with key: %s' % wssk)

    if not isinstance((session, 'Session')):
        raise endpoints.NotFoundException('No Session Found With Key')

    return session
