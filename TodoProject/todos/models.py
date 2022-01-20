from django.db import models

# Create your models here.
class Todo(models.Model):
    content = models.TextField()

    

# class UserLogin(models.Model):
#     user = models.ForeignKey(models.CASCADE, name=True)