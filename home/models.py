from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_owner=models.BooleanField('Is owner', default=False)
    is_customer=models.BooleanField('Is customer', default=False)
    
class Product(models.Model):
    productName=models.CharField(max_length = 200)
    def __str__(self):
        return self.productName
  
 
class fpRecord(models.Model):
    date=models.DateField(default=datetime.now)
    
class Fp(models.Model):
    support=models.FloatField()
    itemsets=models.BinaryField()
    key=models.ForeignKey(fpRecord,on_delete=models.CASCADE,related_name="recordKey")    
    
class associationRecord(models.Model):
    fpKey = models.OneToOneField(fpRecord, on_delete=models.CASCADE)
    

class association(models.Model):
    key=models.ForeignKey(associationRecord,on_delete=models.CASCADE,related_name="associationKey")
    antecedents=models.BinaryField()
    consequents=models.BinaryField()
    lift=models.FloatField()
    confidence=models.FloatField()
    support=models.FloatField()
        
       
    
class Billing(models.Model):
    bill=models.BinaryField()   







class fpgrowth(models.Model):
    support=models.FloatField()
    itemsets=models.BinaryField()
    key=models.ForeignKey(fpRecord,on_delete=models.CASCADE,related_name="fpKey")
    
    def __str__(self):
        return self.support