from datetime import datetime

from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from open_ipam.models import ApiKeyToken


class ApiKeyAuthentication(TokenAuthentication):

    def get_token_from_auth_header(self, auth):
        auth = auth.split()
        # print(auth)
        if not auth or auth[0].lower() != b'api-key':
            return AuthenticationFailed('Invalid api-key header. No credentials provided.')

        if len(auth) == 1:
            raise AuthenticationFailed('Invalid api-key header. No credentials provided.')
        elif len(auth) > 2:
            raise AuthenticationFailed('Invalid api-key header. Token string should not contain spaces.')

        try:
            return auth[1].decode()
        except UnicodeError:
            raise AuthenticationFailed('Invalid api-key header. Token string should not contain invalid characters.')

    def authenticate(self, request):
        auth = get_authorization_header(request)
        token = self.get_token_from_auth_header(auth)

        if not token:
            token = request.GET.get('api-key', request.POST.get('api-key', None))

        if token:
            return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        try:
            token = ApiKeyToken.objects.get(key=key)
        except ApiKeyToken.DoesNotExist:
            raise AuthenticationFailed(code=403, detail='Invalid Api key.')

        if not token.is_active:
            raise AuthenticationFailed(code=403, detail='Api key inactive or deleted.')
        if token.expireTime < datetime.now():
            raise AuthenticationFailed(code=401, detail='Api key is expired')
        # user = token.company.users.first()  # what ever you want here
        return token
