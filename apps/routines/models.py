from django.conf import settings
from django.db import models
from common.models import TimeStampedModel

class Habit(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    name = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)
    
    class Meta(TimeStampedModel.Meta):
        constraints = [
            models.UniqueConstraint(fields=["owner", "name"], name="unique_habit_owner_name")
        ]
        
    def __str__(self) -> str:
        return self.name
    
class HabitCheckin(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habit_checkins")
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name="checkins")
    day = models.DateField(db_index=True)
    done = models.BooleanField(default=False)
    note = models.CharField(max_length=160, blank=True)
    
    class Meta(TimeStampedModel.Meta):
        constraints = [
            models.UniqueConstraint(fields=["owner", "habit", "day"], name="uniq_checkin_per_day")
        ]
        
    def __str__(self) -> str:
        return f"{self.habit} @ {self.day}"