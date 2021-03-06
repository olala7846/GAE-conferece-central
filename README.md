# Conference Centrol
Conference centrol site using App Engine and Cloud endpoint.
**WARNING!** This is project 4 of the udacity full-stack nanodegree, be careful if you want to do it yourself.

Cloned from Udacity and modified by olala7846@gmail.com

hosted [here:](https://olala-udacity-projects.appspot.com/)

## Framework and language
- [App Engine][1]
- [Python][2]
- [Google Cloud Endpoints][3]

## Setup Instructions
1. Update the value of `application` in `app.yaml` to the app ID you
   have registered in the App Engine admin console and would like to use to host
   your instance of this sample.
1. Update the values at the top of `settings.py` to
   reflect the respective client IDs you have registered in the
   [Developer Console][4].
1. Update the value of CLIENT_ID in `static/js/app.js` to the Web client ID
1. (Optional) Mark the configuration files as unchanged as follows:
   `$ git update-index --assume-unchanged app.yaml settings.py static/js/app.js`
1. Run the app with the devserver using `dev_appserver.py DIR`, and ensure it's running by visiting your local server's address (by default [localhost:8080][5].)
1. (Optional) Generate your client library(ies) with [the endpoints tool][6].
1. Deploy your application.

## Test instruction
No unit test implemented, but if you want to test locally,
use `/mock/mock_conference_data` to test your UI

## Udacity project Detail

### Task 1: Session
* The `Session` class was created to be a child of `Conference` class thus we can easily query all sessions in the same conference.
* `Session.sessionType` is a `StringProperty()` as ndb model and `enumFeild()` as protorpc message
* `date` and `time` are stored seperately in ndb as `DateProperty()` and `TimeProperty()` 

### Task 2: Wishlist
* `addSessionToWishlist` implemented
* `getSessionsInWishlist` implemented

### Task 3: Query and indices
#### Additional querry
* `upcomingConferences` shows the latest conferences which haven't started order by time
* `getConferenceAttendee` get all the attendee profile

#### Query Problem

**Problem:**

Let’s say that you don't like workshops and you don't like sessions after 7 pm. How would you handle a query for all non-workshop sessions before 7 pm? What is the problem for implementing this query? What ways to solve it did you think of?

**Answer:**

it is impossible to do inequality filter (not WORKSHOP) on `sessionType` and sort by `time` at the same time on Google ndb, because it is actually two inequality filter on different `Proprty` of the same `Entity`.
To solve this problem we could simply fetch all non-WORKSHOP sessions and loop through it to filter unwanted sessions time or fetch by `time` then loop throught it to filter `sessionType`

### Task 4: Add a Task
* `getFeaturedSpeaker()` implemented
* will check for featured speakers when `createSession` called

[1]: https://developers.google.com/appengine
[2]: http://python.org
[3]: https://developers.google.com/appengine/docs/python/endpoints/
[4]: https://console.developers.google.com/
[5]: https://localhost:8080/
[6]: https://developers.google.com/appengine/docs/python/endpoints/endpoints_tool
