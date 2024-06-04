from django.db import models
import datetime

class ShowManager(models.Manager):
    def show_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2:
            errors['title'] = "The title should be at least 2 characters."
        if len(postData['network']) < 2:
            errors['network'] = "The network should be at least 2 characters."
        if 'date' in postData and postData['date']:
            release_date = datetime.datetime.strptime(postData['date'], '%Y-%m-%d')
            today_date = datetime.datetime.today()
            if today_date < release_date:
                errors['date'] = "Date should be in the past!"
        else:
            errors['date'] = "Date field is required!"
        if 0 < len(postData['description']) < 10:
            errors["description"] = "Description should be at least 10 characters."
        return errors

class Show(models.Model):
    title = models.CharField(max_length=255)
    network = models.CharField(max_length=255)
    date = models.DateField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ShowManager()

    def __str__(self):
        return self.title
