from django.db import models
from users.models import CustomUser
from events.models import Event

RARITY_CHOICES = [
    ('common', 'Common'),
    ('uncommon', 'Uncommon'),
    ('rare', 'Rare'),
    ('ultra_rare', 'Ultra Rare'),
    ('one_in_hundred', '1/100'),
    ('one_in_ten', '1/10'),
    ('one_in_one', '1/1'),
]

class Figure(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='figures/')
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='figures')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_rarity_display()}) - {self.event.name}"

class Album(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='albums')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='albums')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.owner.username}'s Album for {self.event.name}"
    
    class Meta:
        unique_together = ('event', 'owner')

class UserFigure(models.Model):
    figure = models.ForeignKey(Figure, on_delete=models.CASCADE, related_name='user_figures')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='figures')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='figures')
    obtained_at = models.DateTimeField(auto_now_add=True)
    is_for_sale = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.owner.username}'s {self.figure.name}"
    
    class Meta:
        ordering = ['-obtained_at']

class FigurePackage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='packages')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Package for {self.event.name} - ${self.price}"
