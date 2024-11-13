from django.db import models
from django.forms import ValidationError
from django.utils.timezone import now


class Meeting(models.Model):
    owner = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="meeting_owner")
    guest = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, related_name="meeting_guest", null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    description = models.TextField(null=True, blank=True)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time.")
        if self.start_time < now():
            raise ValidationError("You cannot schedule a meeting in the past.")

        overlapping_meetings = Meeting.objects.filter(
            guest=self.guest,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        )
        
        if overlapping_meetings.exists():
            raise ValidationError(f"{self.guest} already has a meeting scheduled in this time slot.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.start_time} - {self.end_time}: {self.owner} -> {self.guest}"
