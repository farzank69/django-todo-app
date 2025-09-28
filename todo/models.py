from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    CATEGORY_CHOICES = [
        ('Work', 'Work'),
        ('Personal', 'Personal'),
        ('School', 'School'),
        ('Shopping', 'Shopping'),
        ('Other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE) #this will link my task to user 
    title = models.CharField(max_length=200)                 #its the title
    description = models.TextField(blank=True, null=True)    #optional desc if user wants to add.
    due_date = models.DateField(blank=True, null=True)
    priority = models.CharField(
        max_length=10,
        choices = [
            ("High", "High"),
            ("Medium", "Medium"),
            ("Low", "Low"),
        ],
        default="Medium"
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default = 'Other', null=True)
    completed = models.BooleanField(default=False)           # you can mark it done/not done.
    created_at = models.DateTimeField(auto_now_add=True)     # timestamp

    def __str__(self):
        return self.title


