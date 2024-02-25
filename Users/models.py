from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    current_weight = models.FloatField()
    height = models.FloatField()
    ACTIVITY_LEVEL_CHOICES = [
        ('not_very_active', 'Not Very Active'),
        ('moderately_active', 'Moderately Active'),
        ('very_active', 'Very Active'),
    ]
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    
    GOAL_CHOICES = [
        ('maintain_weight', 'Maintain Weight'),
        ('gain_weight', 'Gain Weight'),
        ('lose_weight', 'Lose Weight'),
    ]
    
    goal = models.CharField(max_length=20,default='maintain_weight', choices=GOAL_CHOICES)

    def __str__(self):
        return self.user.username
    
    # models.py


class DailyCaloriesConsumed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    food_name = models.TextField(default = "no_name")
    calories_consumed = models.PositiveIntegerField()
    protein = models.PositiveIntegerField(default=0 )
    carbs = models.PositiveIntegerField(default = 0)
    fat = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.time}"

class TotalDailyCaloriesConsumed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    total_calories_consumed = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"



