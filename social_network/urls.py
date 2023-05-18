from django.urls import path
from .views import (
    FriendListView,
    FriendRequestUpdateView,
    UserSearchView,
    FriendRequestCreateView,
    FriendRequestListView,
    FriendRequestPendingListView,
    UserSignupView
)
from .views import UserLoginView

urlpatterns = [
    path('users/search/', UserSearchView.as_view(), name='user-search'),

    # Friend request endpoints
    path('friend-requests/', FriendRequestCreateView.as_view(), name='send-friend-request'),
    path('friend-requests/<int:pk>/', FriendRequestUpdateView.as_view(), name='update-friend-request'),
    path('friend-requests/pending/', FriendRequestPendingListView.as_view(), name='pending-friend-requests'),

    # Friend list
    path('friends/', FriendListView.as_view(), name='friend-list'),

    # Authentication endpoints
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('signup/', UserSignupView.as_view(), name='user-signup'),

]
