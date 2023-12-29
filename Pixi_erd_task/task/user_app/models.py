from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.deletion.CASCADE, related_name='profile')
    is_buyer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return f"User: {self.user.first_name}, Buyer: {self.is_buyer}, Seller: {self.is_seller}"