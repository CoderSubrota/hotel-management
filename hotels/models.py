
from django.db import models
from users.models import UserProfile
from django.utils import timezone

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    image = models.ImageField(upload_to='hotels_images/')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available_rooms = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Booking by {self.user.username} for {self.hotel.name}"
     
class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_id = models.CharField(max_length=255)
    hotel_name = models.CharField(max_length=522)
    created_at = models.DateTimeField(auto_now_add=True)
    check_in = models.DateTimeField(default="2025-02-20")  
    check_out = models.DateTimeField(default="2025-02-25")  

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.created_at}"
    