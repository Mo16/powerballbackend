from django.db import models

# Create your models here.
class First_prize(models.Model):
    bnb = models.TextField(max_length=200, null=True,blank=True)

    def __str__(self):
        return self.bnb
    

class Second_prize(models.Model):
    bnb = models.TextField(max_length=200, null=True,blank=True)

    def __str__(self):
        return self.bnb
    

class Third_prize(models.Model):
    bnb = models.TextField(max_length=200, null=True,blank=True)

    def __str__(self):
        return self.bnb
    
