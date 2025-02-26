from rest_framework.response import Response
from rest_framework import viewsets, status
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from rest_framework.views import APIView
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.contrib.auth.tokens import default_token_generator
from .serializers import UserSerializer



User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        return Response({"detail": "Creation is not allowed."}, status=status.HTTP_403_FORBIDDEN)
    


class UserActivationView(APIView):
    def get(self, request, uid, token):
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({"success": _("User activated successfully.")}, status=status.HTTP_200_OK)
        else:
            return Response({"error": _("Activation link is invalid.")}, status=status.HTTP_400_BAD_REQUEST)