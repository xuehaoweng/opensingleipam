import datetime

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from IpamV1 import settings
from utils.crypt_pwd import CryptPwd

EXPIRE_MINUTES = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES', 1)


class ObtainExpiringAuthToken(ObtainAuthToken):
    """Create user token"""

    def post(self, request):
        # print(request.data)
        # password = request.data.copy().get("password")[0]
        # print(request.data.copy()["password"])
        # request.data.copy()["password"] = CryptPwd().de_js_encrypt(password.replace(' ',"+"))
        # print(request.data.copy()["password"])
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
            time_now = datetime.datetime.now()
            if created or token.created < time_now - datetime.timedelta(minutes=EXPIRE_MINUTES):
                # Update the created time of the token to keep it valid
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = time_now
                token.save()
            return Response({'code': 200, 'data': {
                'token': token.key
            }}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()
