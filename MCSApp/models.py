from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
	
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	user_role = models.CharField(max_length=100)

	
class dataset(models.Model):
	cust_id = models.IntegerField()
	gender = models.CharField(max_length=100)
	age = models.IntegerField()
	income = models.IntegerField()
	spending_s = models.IntegerField()
	cluster = models.IntegerField(default = 0)

# class dataset2(models.Model):
# 	cust_id = models.IntegerField()
# 	gender = models.CharField(max_length=100)
# 	age = models.IntegerField()
# 	income = models.IntegerField()
# 	spending_s = models.IntegerField()
# 	cluster = models.IntegerField(default = 0)