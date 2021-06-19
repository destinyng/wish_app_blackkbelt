from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):

    def registration_validator(self, post_data):
        errors = {}
        email_in_use = User.objects.filter(email = post_data['email'])
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters.'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters.'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):        
            errors['email'] = "Invalid email address."
        if len(post_data['email']) > 255:
            errors['email'] = 'Email address is too long.'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long.'
        if post_data['password'] != post_data['confirm_password']:
            errors['confirm_password'] = 'Passwords do not match.'
        if len(email_in_use) !=0:
            errors['unique'] = 'This email is already associated with an account.'
        return errors

    def login_validator(self, post_data):
        errors = {}
        if len(post_data['email']) < 1:
            errors['email'] = 'Email is required'
        if len(post_data['password']) < 1:
            errors['password'] = 'Password is required'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    granted_wishes = models.IntegerField(default=0)
    pending_wishes = models.IntegerField(default=0)

    objects = UserManager()



class WishManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        #postData == request.POST
        if len(postData['name']) < 3:
            errors['name'] ='Name must be at least 3 characters long.'
        if len(postData['description']) < 3:
            errors['description'] ='Description must be at least 3 characters long.'
        return errors

class Wish(models.Model):
    name = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    wished_by = models.ForeignKey(User,related_name='wishes', on_delete=models.CASCADE)
    user_that_like_wish= models.ManyToManyField(User, related_name='users_liked')
    is_granted =models.BooleanField()
    created_at = models.DateTimeField(auto_now_add = True)
    granted_at = models.DateTimeField(auto_now = True)
  
    objects = WishManager()




    

