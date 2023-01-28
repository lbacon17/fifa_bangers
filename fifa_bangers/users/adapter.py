from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        path = "../../"
        return path.format()

    def get_logout_redirect_url(self, request):
        path = "../../"
        return path.format()
