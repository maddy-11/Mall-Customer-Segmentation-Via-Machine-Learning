from django.db import models
from django.contrib.auth.models import User
from MCSApp.models import *
# Create your models here.
class customer(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	c_data = models.ForeignKey(dataset, on_delete=models.CASCADE, null=True)
	user_role = models.CharField(max_length=100)

class products(models.Model):
	p_name = models.CharField(max_length=100)
	p_desc = models.TextField()
	p_rattings = models.IntegerField()
	p_image = models.CharField(max_length=200)
	p_cat = models.CharField(max_length=100)
	p_cat2 = models.CharField(max_length=100,null=True)
	p_price = models.IntegerField(null = True)
	p_quantity = models.IntegerField(null=True)

class orders(models.Model):
	p_id = models.ForeignKey(products,on_delete=models.CASCADE)
	u_id = models.ForeignKey(User,on_delete=models.CASCADE)
	color = models.CharField(max_length=100)
	quantity = models.IntegerField()
	price = models.IntegerField(null = True)
	t_amount = models.IntegerField(null = True)
	delivery_status = models.CharField(max_length=50, null=True)

class vouchers(models.Model):
	voucher = models.CharField(max_length=100)
	percentage = models.IntegerField(null = True)
	category = models.CharField(max_length=100,null=True)

class newsletter(models.Model):
	email = models.EmailField(max_length = 254)

class notifications(models.Model):
	message = models.TextField()
	category = models.CharField(max_length=100)
	date = models.DateTimeField(auto_now_add=True,null=True)

class review(models.Model):
	r_name = models.CharField(max_length=100)
	review = models.TextField()
	rattings = models.IntegerField()
	p_id = models.ForeignKey(products,on_delete=models.CASCADE)
	u_id = models.ForeignKey(User,on_delete=models.CASCADE)

class d_address(models.Model):
	address = models.TextField()
	city = models.CharField(max_length=100)
	province = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)
	order = models.ForeignKey(orders,on_delete=models.CASCADE,null=True)

class card(models.Model):
	c_name = models.CharField(max_length=100)
	c_num = models.CharField(max_length=100)
	c_month = models.CharField(max_length=100)
	c_year = models.CharField(max_length=100)
	cvv = models.IntegerField()

class recommendation(models.Model):
	cluster = models.IntegerField()
	p_name = models.CharField(max_length=100)

