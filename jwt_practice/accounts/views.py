from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer

User =  get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer =  RegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
        
            refreshToken = RefreshToken.for_user(user)
            accessToken = str(refreshToken.access_token)

            return Response(
            {   "email": user.email,
                'Message':"Creation Success",
                "User_access_Token" : accessToken
            },
            status= status.HTTP_201_CREATED
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)