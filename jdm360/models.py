from django.db import models
import re


class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['fname']) < 2:
            errors['fname'] = 'First Name field should be at least 2 characters'
        if len(postData['lname']) < 2:
            errors['lname'] = 'Last Name field should be at least 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Email must be a valid format!"
        if len (postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!!"
        if postData['password'] != postData['conf_password']:
            errors ['conf_password'] = "Passwords do not match"
        return errors

class Users(models.Model):
    fname = models.CharField(max_length=45)
    lname = models.CharField(max_length=45)
    email = models.EmailField()
    password = models.CharField(max_length=155)
    classification = models.CharField(max_length=100, default="client")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Locations(models.Model):
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    zipcode = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Orders(models.Model):
    location = models.ForeignKey(Locations, related_name='order', on_delete=models.CASCADE)
    package = models.CharField(max_length=25)
    orderdate = models.DateTimeField()
    comments = models.CharField(max_length=255)
    client = models.ForeignKey(Users, related_name="order", on_delete=models.CASCADE)
    photographer = models.CharField(max_length=255)
    status = models.CharField(max_length=25, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 