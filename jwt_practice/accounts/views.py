from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate
from .serializers import RegisterSerializer,LoginSerializer

User =  get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer =  RegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
        
            # refreshToken = RefreshToken.for_user(user)
            # accessToken = str(refreshToken.access_token)

            return Response(
            {   "email": user.email,
                'Message':"Creation Success",
                # "User_access_Token" : accessToken
            },
            status= status.HTTP_201_CREATED
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)  # Corrected `request.date` to `request.data`
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)

            if user is None:
                return Response({'error': 'Invalid Creds'}, status=status.HTTP_401_UNAUTHORIZED)  # Fixed the error with the response format
            
            refresh_token = RefreshToken.for_user(user)
            access_token = str(refresh_token.access_token)

            return Response(
                {
                    "Message": "Login Success",
                    "email": user.email,
                    "access": access_token
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
