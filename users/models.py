from django.contrib.auth.models import AbstractUser
from django.db import models

class UserProfile(AbstractUser):
    first_name=models.TextField(max_length=652)
    last_name=models.TextField(max_length=652)
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    balance=models.TextField()
    

    # Adding related_name to resolve the naming conflict
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
    )

    def __str__(self):
        return self.username


