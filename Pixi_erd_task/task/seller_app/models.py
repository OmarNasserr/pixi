from django.db import models
from user_app.models import UserProfile


class Seller(models.Model):
    user_id = models.OneToOneField(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return f"Seller: {self.user_id.user.first_name}"