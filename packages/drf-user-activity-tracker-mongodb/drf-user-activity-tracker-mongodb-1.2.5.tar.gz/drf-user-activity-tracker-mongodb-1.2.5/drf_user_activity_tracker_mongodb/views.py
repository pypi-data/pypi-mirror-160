from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_user_activity_tracker_mongodb.permissions import CanViewAdminHistory
from drf_user_activity_tracker_mongodb.serializers import ActivityLogSerializer, ActivityLogAdminSerializer
from drf_user_activity_tracker_mongodb.utils import MyCollection


class ActivityLogView(mixins.ListModelMixin, GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ActivityLogSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return MyCollection().list(user_id=self.request.user.id, api=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ActivityLogAdminView(mixins.ListModelMixin, GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CanViewAdminHistory]
    serializer_class = ActivityLogAdminSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return MyCollection().list(api=True)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
