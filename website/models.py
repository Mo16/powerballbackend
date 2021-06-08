from django.db import models

# Create your models here.
class First_prize(models.Model):
    name = models.CharField(max_length=200, null=True,blank=True)
    bnb = models.CharField(max_length=200, null=True,blank=True)

    def __str__(self):
        return self.name
    

class Second_prize(models.Model):
    name = models.CharField(max_length=200, null=True,blank=True)
    bnb = models.CharField(max_length=200, null=True,blank=True)

    def __str__(self):
        return self.name
    

class Third_prize(models.Model):
    name = models.CharField(max_length=200, null=True,blank=True)
    bnb = models.CharField(max_length=200, null=True,blank=True)


    def __str__(self):
        return self.name
    

