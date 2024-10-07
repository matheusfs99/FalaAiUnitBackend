from rest_framework import serializers

from apps.accounts.models import User
from .models import Meeting
from datetime import datetime
from apps.accounts.serializers import UserNameSerializer


class CustomDateTimeField(serializers.DateTimeField):
    def to_internal_value(self, data):
        try:
            return datetime.strptime(data, "%d/%m/%Y %H:%M:%S")
        except ValueError:
            raise serializers.ValidationError("Formato inválido para data e hora. Use DD/MM/YYYY HH:mm:ss.")


class MeetingSerializer(serializers.ModelSerializer):
    start_time = CustomDateTimeField()
    end_time = CustomDateTimeField()
    guest = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Meeting
        fields = ['id', 'owner', 'guest', 'description', 'start_time', 'end_time']
        extra_kwargs = {"owner": {"read_only": True}}
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = UserNameSerializer(instance.owner).data
        representation['guest'] = UserNameSerializer(instance.guest).data
        return representation

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("End time must be after start time.")
        
        overlapping_meetings = Meeting.objects.filter(
            guest=data['guest'],
            start_time__lt=data['end_time'],
            end_time__gt=data['start_time']
        )
        
        if overlapping_meetings.exists():
            raise serializers.ValidationError(f"The guest already has a meeting during this time.")
        
        return data

    def create(self, validated_data):
        meeting = Meeting.objects.create(**validated_data)
        return meeting
