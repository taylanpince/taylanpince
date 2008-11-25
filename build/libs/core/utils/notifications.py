'''
simple middleware and context processor for session-based messaging with types
Heavily inspired by patches on ticket 4604. Differs in that in this a notification
has type.

Installation:
add notifications.NotificationMiddleware to MIDDLEWARE_CLASSES
and notifications.notifications to TEMPLATE_CONTEXT_PROCESSORS

That assumes notifications.py is on pythonpath. If notifications.py lives in
your project dir, prefix those with '(projectname).'

Example use:
request.notifications.create('Some bland information message.')
request.notifications.create('Some more exciting error message.', 'error')

Example template code:
{% if notifications %}
<ul id="notifications">
    {% for notification in notifications %}<li class="{{ notification.type }}">{{ notification.content }}</li>
    {% endfor %}
</ul>
{% endif %}

Example styling:
points to names of famfam icons and assumes structure like 
#notifications, #notifications li {
  list-style: none;
  list-style-type: none;
  margin-left: 0;
}
.information, .error, .success, .warning {
  margin-top: 0.4em;
  border: 1px solid #9bb8d9;
  padding: 6px 6px 6px 30px;
}
.information {
  background: #dedfff url('../icons/information.png') 6px 50% no-repeat;
  color: #406299;
}
.error {
  background: #ffe1da url('../icons/exclamation.png') 6px 50% no-repeat;
  border-color: #f34f4f;
  color: #be0b0b;
}
.success {
  background: #e2f9e3 url('../icons/accept.png') 6px 50% no-repeat;
  border-color: #9c9;
  color: #080;
}
.warning {
  background:#fff8bf url('../icons/error.png') 6px 50% no-repeat;
  border-color: #ffd324;
  color:#eb830c;
}
'''

from django.utils.encoding import StrAndUnicode

DEFAULT_TYPE = 'information'

class NotificationMiddleware:
    def process_request(self, request):
        request.__class__.notifications = Notifications(request.session)
        return None

class Notifications:
    def __init__(self, session):
        self.session = session
        self.SESSION_VARIABLE = '_notifications'

    def get(self):
            return self.session.get(self.SESSION_VARIABLE, [])
    
    def get_and_clear(self):
            return self.session.pop(self.SESSION_VARIABLE, [])
    
    def create(self, message, type=DEFAULT_TYPE):
        """creates a notification
        
        arguments:
        message: text content of notification
        type: optional type (defaults to the value of DEFAULT_TYPE)
        """
        notifications = self.session.get(self.SESSION_VARIABLE)
        if notifications is None:
            notifications = []
            self.session[self.SESSION_VARIABLE] = notifications
        notifications.append({'content': message, 'type': type})
        self.session.modified = True

def notifications(request):
    """
    Returns notifications for the session and the current user.

    Note that this processor is only useful to use explicity if you are not
    using the (enabled by default) auth processor, as it also provides the
    notifications (by calling this method).

    The notifications are lazy loaded, so no notifications are retreived and deleted
    unless requested from the template.

    Both contrib.session and contrib.auth are optional. If neither is provided,
    no 'notifications' variable will be added to the context.
    """
    if hasattr(request, 'session') or hasattr(request, 'user'):
        return {'notifications': LazyNotifications(request)}
    return {}

class LazyNotifications(StrAndUnicode):
    """
    A lazy proxy for session and authentication notifications.
    """
    def __init__(self, request):
        self.request = request

    def __iter__(self):
        return iter(self.notifications)

    def __len__(self):
        return len(self.notifications)

    def __nonzero__(self):
        return bool(self.notifications)

    def __unicode__(self):
        return unicode(self.notifications)

    def __getitem__(self, *args, **kwargs):
        return self.notifications.__getitem__(*args, **kwargs)

    def _get_notifications(self):
        if hasattr(self, '_notifications'):
            return self._notifications

        # First, retreive any notifications for the user.
        if hasattr(self.request, 'user') and \
           hasattr(self.request.user, 'get_and_delete_messages'):
            self._notifications = [{'content': message, 'type': DEFAULT_TYPE} for
                message in self.request.user.get_and_delete_messages()]
        else:
            self._notifications = []

        # Next, retrieve any notifications for the session.
        if hasattr(self.request, 'session'):
            self._notifications += self.request.notifications.get_and_clear()
        return self._notifications
    notifications = property(_get_notifications)
