import json
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings



class RichAdapter(DefaultSocialAccountAdapter):
    def populate_user(self,
                      request,
                      sociallogin,
                      data):
        """
        Hook that can be used to further populate the user instance.

        For convenience, we populate several common fields.

        Note that the user instance being populated represents a
        suggested User instance that represents the social user that is
        in the process of being logged in.

        The User instance need not be completely valid and conflict
        free. For example, verifying whether or not the username
        already exists, is not a responsibility.
        """
        user = super(RichAdapter, self).populate_user(request, sociallogin, data)
        extra_data = sociallogin.account.extra_data
        for field_name, field_data in extra_data.iteritems():
            if hasattr(user, 'facebook_%s' % field_name):
                setattr(user, 'facebook_%s' % field_name, json.dumps(field_data))
        return user
