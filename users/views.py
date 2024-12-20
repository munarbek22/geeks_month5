from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer, ConfirmationCodeSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmationCode

@api_view(['POST'])
def authorization_ap_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password, is_active=False)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data('username')
    password = serializer.validated_data('password')

    user = User.objects.create_user(username=username, password=password)

    return Response(data={'user_id': user.id}, status=status.HTTP_201_CREATED)


# User Confirmation
@api_view(['POST'])
def confirmation_api_view(request):
    serializer = ConfirmationCodeSerializer(data=request.data)
    if serializer.is_valid():
        try:
            confirmation = ConfirmationCode.objects.get(code=serializer.validated_data['code'])
            user = confirmation.user
            user.is_active = True
            user.save()
            confirmation.delete()
            return Response({"message": "Account confirmed successfully."}, status=status.HTTP_200_OK)
        except ConfirmationCode.DoesNotExist:
            return Response({"error": "Invalid confirmation code."}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

