from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework_simplejwt.tokens import RefreshToken
from.serializers import UserSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response(get_tokens_for_user(user), status=status.HTTP_201_CREATED)
class ProtectedView(generics.RetrieveAPIView):
   
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'You have access to this protected route'})
        

# Create your views here.
