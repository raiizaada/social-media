from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import  FriendRequest
from social_network.serializers import UserSerializer, FriendRequestSerializer, UserSignupSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework.pagination import PageNumberPagination



class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10

    def get_queryset(self):
        search_keyword = self.request.query_params.get('keyword', '')
        if '@' in search_keyword:  
            return User.objects.filter(email__iexact=search_keyword)
        else:  
            return User.objects.filter(username__icontains=search_keyword)
        
    def paginate_queryset(self, queryset):
        return super().paginate_queryset(queryset)[:10]

class FriendRequestCreateView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
       
        return super().create(request, *args, **kwargs)

class FriendRequestListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user.id
        return FriendRequest.objects.filter(from_user=user, status='accepted')

class FriendRequestPendingListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        user = self.request.user.id
        return FriendRequest.objects.filter(to_user=user, status='pending')



class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
      
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user_id=user.id)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer


class FriendRequestCreateView(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        
        user = request.user.id
        current_time = timezone.now()
        one_minute_ago = current_time - timedelta(minutes=1)
        friend_requests_count = FriendRequest.objects.filter(from_user=user, created_at__gte=one_minute_ago).count()

        if friend_requests_count >= 3:
            return Response({'error': 'You have exceeded the limit of 3 friend requests within a minute.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        return super().create(request, *args, **kwargs)


class FriendRequestUpdateView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        friend_request = self.get_object()
        friend_request.status = request.data.get('status')
        friend_request.save()
        return Response({'status': friend_request.status})


class FriendListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user.id
        return FriendRequest.objects.filter(from_user=user, status='accepted')


class FriendRequestPendingListView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]  

    def get_queryset(self):
        user = self.request.user.id
        return FriendRequest.objects.filter(to_user=user, status='pending')
