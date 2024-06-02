from django.db import models

# Create your models here.
class subscriber(models.Model):
    FullName = models.CharField(max_length = 250, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True,unique=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    createdat = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'subscriber'

class car_details(models.Model):
    carimage = models.ImageField(upload_to='carimages')
    name = models.CharField(max_length = 250, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    seats = models.IntegerField()
    fuel = models.CharField(max_length=100, blank=True, null=True)
    mileage = models.CharField(max_length=100, blank=True, null=True)
    luggage = models.CharField(max_length=250, blank=True, null=True)
    descripton = models.CharField(max_length=250, blank=True, null=True)
    features = models.CharField(max_length=250, blank=True, null=True)
    addedat = models.DateTimeField(auto_now_add=True)
    rent_amount = models.CharField(max_length=100, blank=True, null=True)
    is_available = models.BooleanField(default=True)


    class Meta:
        db_table = 'car_details'


class car_booking(models.Model):
    carimage = models.ImageField(upload_to='carimages')
    car_name = models.CharField(max_length = 250, blank=True, null=True)
    customer_name = models.CharField(max_length = 250, blank=True, null=True)
    customer_username = models.CharField(max_length = 250, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    booking_from = models.DateTimeField(blank=True, null=True)
    booking_to = models.DateTimeField(blank=True, null=True)
    confirm_at = models.DateTimeField(blank=True, null=True)
    booking_status = models.BooleanField(default=False)
    journey_status = models.BooleanField(default=False)
    


    class Meta:
        db_table = 'car_booking'