from django.db import models
from Users.models import User
# Create your models here.

class LikedRecipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe_name = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()

    def __str__(self):
        return self.recipe_name