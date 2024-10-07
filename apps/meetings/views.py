from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Meeting
from .serializers import MeetingSerializer
from datetime import datetime
from django.db.models import Q

class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(Q(owner=user) | Q(guest=user), end_time__gt=datetime.now())

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
