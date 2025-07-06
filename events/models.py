from django.db import models
from users.models import CustomUser
from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_events')
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    
    def is_currently_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date
    
    class Meta:
        ordering = ['-start_date']
