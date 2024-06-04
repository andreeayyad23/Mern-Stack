from django.db import models
import datetime
import bcrypt
import re

class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        
        # Validate destination
        if 'destination' not in postData or len(postData['destination']) < 2:
            errors['destination'] = "Destination must be at least 8 characters long!"
        
        # Validate itinerary
        if 'itinerary' not in postData:
            errors['itinerary'] = "Itinerary is required."
        elif len(postData['itinerary']) > 50:
            errors['itinerary'] = "Itinerary must be 50 characters or fewer."
        
        # Validate dates
        if 'start_date' not in postData or 'end_date' not in postData:
            errors['date'] = "Start date and end date are required."
        else:
            try:
                start_date = datetime.datetime.strptime(postData['start_date'], '%Y-%m-%d')
                end_date = datetime.datetime.strptime(postData['end_date'], '%Y-%m-%d')
                if start_date >= end_date:
                    errors['date'] = "Start date must be before end date."
            except ValueError:
                errors['date'] = "Invalid date format. Use YYYY-MM-DD."

        return errors

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}

        if len(postData['firstname']) < 2:
            errors['firstname'] = "The first name should be at least 2 characters."

        if len(postData['lastname']) < 2:
            errors['lastname'] = "The last name should be at least 2 characters."

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):  
            errors['email'] = "Invalid email address!"
        else:
            try:
                email = User.objects.get(email__iexact=postData['email'])
                errors['email'] = "The email is taken please try another one"
            except User.DoesNotExist:
                pass

        if len(postData['password']) < 8:
            errors['password'] = "Password should be at least 8 characters"
        
        if postData['password'] != postData['confirmPW']:
            errors['confirmPW'] = "Password is not equal to the confirm password"
        
        return errors
    
    def login_validator(self, postData):
        errors= {}
        user = User.objects.filter(email= postData['email'])
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']): 
            errors['login_email'] = "Email is not valid"
        elif not user.exists():
            errors['login_email'] = "Email unused"
        else: 
            if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
                errors['login'] = "Email or Password is incorrect !"
                
        return errors

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    travelers = models.ManyToManyField(User, related_name="trips")
    itinerary = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organizer = models.ForeignKey(User, related_name="user_trips", on_delete=models.CASCADE)
    objects = TripManager()
