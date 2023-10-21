from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import pandas as pd
from .models import *
from estore.models import *
from estore.models import customer
from .utils import *
from django.db.models import Q

# Create your views here.

# pages
def home(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			order = orders.objects.all()
			order2 = order.exclude(delivery_status="Order Pending")
			order3 = order.filter(delivery_status="Order Pending")
			c = customer.objects.all().count()
			v = vouchers.objects.all().count()
			p = products.objects.all().count
			do = order.filter(delivery_status='Delivered').count()
			dt = order.filter(Q(delivery_status='To be Delivered') | Q(delivery_status='Out For Delivery')).count()
			if do is None:
				do = 0
			if dt is None:
				dt = 0

			context = {'dt':dt,'do':do,'o':order.count(),'order':order2,'order3':order3,'c':c,'v':v,'p':p}

			return render(request,'home.html',{'context':context})
		else:
			messages.warning(request, 'Not an Admin')
			return redirect('/panel/login')
	else:
			messages.warning(request, 'Not Sign-In')
			return redirect('/panel/login')

def users(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			data = Account.objects.all()
			data1 = customer.objects.all()
			data2 = User.objects.all()
			return render(request,'users.html',{'data' : data,'data1' : data1,'data2' : data2})
		else:
			messages.warning(request, 'Not Sign-In')
			return redirect('/panel/login')
	else:
		messages.warning(request, 'Not Sign-In')
		return redirect('/panel/login')

# APIs
def register_(request):
	user = request.user
	if user.is_authenticated:
		abc = user.username
		if abc == "admin":
			if request.method == 'POST':
				username = request.POST['name']
				email = request.POST['email']
				pass_ = request.POST['pass']
				q = User.objects.create_user(username, email, pass_)
				q.save()
				user = User.objects.get(username = username)
				query = Account(user = user,user_role = 'Employee')
				query.save()
				return redirect('/panel/users')
			else:
				return render(request,'register.html')
		else:
				messages.warning(request, 'not an Admin')
				return redirect('/panel/login')
	else:
		messages.warning(request, 'Login First')
		return redirect('/panel/login')

def delete(request,pk):
	z = User.objects.get(id = pk)
	user = request.user
	if user.username == 'admin':
		if z.username == 'admin':
			messages.warning(request, 'Cannot Delete Admin')
			return redirect('/panel/users')
	
		z.delete()	
		messages.success(request,'Account Deleted Successfylly')
		return redirect('/panel/users')
	
	messages.warning(request,'Sorry You are not Admin')
	return redirect('/panel/users')

def loginHandle(request):
	if request.method == 'POST':
		username = request.POST['user']
		password = request.POST['pass']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, 'Logged In')
			users = User.objects.get(username=username)
			value = Account.objects.filter(user = users).first()
			request.session['id'] = value.user_role
			return redirect("/panel/")
        
		else:
			messages.warning(request, 'Incorrect')

	return render(request,'login.html')

def logout_(request):
	logout(request)
	return redirect('/store/home/')

# Plottings
def visuals(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			chart = get_cluster_plot()
			return render(request,'Visualization.html',{'chart':chart})
		else:
			messages.warning(request, 'Sign-In')
			return redirect('/panel/login')
	else:
		messages.warning(request, 'Not Signed-In')
		return render(request,'login.html')

def elbow(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			chart = get_elbow()
			return render(request,'Visualization.html',{'chart':chart})
		else:
			messages.warning(request, 'Not Admin')
			return redirect('/panel/login')
	else:
		messages.warning(request, 'Not Signed-In')
		return render(request,'login.html')

def income(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			chart = get_income_plot()
			return render(request,'Visualization.html',{'chart':chart})
		else:
			messages.warning(request, 'Not Admin')
			return redirect('/panel/login')
	else:
		messages.warning(request, 'Not Signed-In')
		return render(request,'login.html')

def spending(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			chart = get_spending_score()
		else:
			messages.warning(request, 'Not Sign-In')
			return redirect('/panel/login')
	return render(request,'Visualization.html',{'chart':chart})

def gender(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			chart = genders()
			return render(request,'Visualization.html',{'chart':chart})
		else:
			messages.warning(request, 'Not Signed In')
			return redirect('/panel/login')
	else:
		messages.warning(request, 'Not Signed-In')
		return render(request,'login.html')

def data(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			chart = customers()
			return render(request,'Visualization.html',{'chart':chart})
		else:
			messages.warning(request, 'Not Signed In')
			return redirect('/panel/login')
	else:
		messages.warning(request, 'Not Signed-In')
		return render(request,'login.html')

def dataset_(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			return render(request,'dataset.html')
		else:
			messages.warning(request, 'Not Signed In')
			return redirect('/panel/login')
	else:
		messages.warning(request, 'Not Signed-In')
		return redirect('/panel/login')

def csvfile(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			if request.method == 'POST':
				files = request.FILES['file']
				location = f"{files}"
				
				d = pd.read_csv(location)
				csv_file = d
				print(d)
				return redirect('/panel/data')
		else:
			messages.warning(request, 'Not Admin')
			return redirect('/panel/login')

	else:
		messages.warning(request, 'Not Signed-In')
		return render(request,'login.html')
	
def report_(request):
	
	report = dataset.objects.all()
	return render(request,'reports.html',{'report':report})

def cluster_(request,cluster):
	cluster = dataset.objects.filter(cluster = cluster)
	report = cluster
	return render(request,'reports.html',{'report':report})

def newsletter_(request):
	email_ = request.POST['subscriber']
	query = newsletter(email = email_)
	query.save()
	return redirect('/')

def notifications_(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			return render(request,'sendnotifications.html',{'cat':"Please Select Any Category",'val':1})
		else:
			messages.warning(request, 'Not an Admin')
			return redirect('/panel/login')
	else:
			messages.warning(request, 'Not Sign-In')
			return redirect('/panel/login')


def notifications1_(request,key):
	print(request.method)
	category = key
	msg = ''
	if request.method == 'POST':
		msg = request.POST['text']
		q = notifications(message=msg,category=category)
		q.save()
	return render(request,'sendnotifications.html',{'cat':category,'val':0})

def view_c_items(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			return render(request,'addcitems.html',{'cat':"Please Select Any Category"})
		else:
			messages.warning(request, 'Not an Admin')
			return redirect('/panel/login')
	else:
			messages.warning(request, 'Not Sign-In')
			return redirect('/panel/login')

def view_c_items1(request,key):

	data = []
	x = recommendation.objects.filter(cluster = key)
	request.session['cat'] = key
	for i in x:
		product = products.objects.filter(p_name = i.p_name).first()
		data.append(product)
	
	return render(request,'addcitems.html',{'data':data,'cat':key})

def add_c_items(request,key):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			x = recommendation.objects.filter(cluster = key)
			cat = 0
			if request.method != 'POST':
				cat = key
				request.session['cat'] = cat
			if request.method == 'POST':
				print("testing123")
				i = request.session['cat']
				p = products.objects.filter(id = key).first()
				check = recommendation.objects.filter(p_name = p.p_name,cluster = i).first()
				if check is None:
					print("in Post")
					q = recommendation(cluster = i,p_name = p.p_name)
					q.save()
				else:
					print("Product Already Present")
				return redirect(f'/panel/viewcategoryitems/{i}')
			data = products.objects.all()
			return render(request,'addcatitems.html',{'data':data,'cat':cat})
		else:
			messages.warning(request, 'Not an Admin')
			return redirect('/panel/login')
	else:
			messages.warning(request, 'Not Sign-In')
			return redirect('/panel/login')

def addvouchers_(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			return render(request,'addvouchers.html')
		else:
			messages.warning(request, 'Not an Admin')
			return redirect('/panel/login')
	else:
			messages.warning(request, 'Not Sign-In')
			return redirect('/panel/login')
def addvouchers(request,key):
	category = key
	msg = ''
	request.session['cat'] = key
	if request.method == 'POST':
		voucher = request.POST['voucher']
		p_age = request.POST['p_age']
		q = vouchers(voucher = voucher, percentage = p_age ,category=category)
		q.save()
	data = vouchers.objects.filter(category = key)
	return render(request,'addvouchers.html',{'data':data,'cat':category,'val':1})

def edititem(request,key):
	a = key
	bags = ['Laptop Bags','Purses','Hiking Bags']
	jewellary = ['Rings','Earings','Necklaces']
	laptops = ['HP','Lenovo','Dell']
	p = products.objects.filter(id = key).first()
	if request.method == 'POST':
		p_name = request.POST['pn']
		p_price = request.POST['pp']
		p_desc = request.POST['pd']
		p_cat = request.POST['category']
		p_cat2 = request.POST['cat2']
		p_quantity = request.POST['q']
		p_image = request.FILES.get('img',None)
		query = products.objects.filter(id = key).first()

		query.p_name = p_name
		query.p_price = p_price
		query.p_cat = p_cat
		query.p_cat2 = p_cat2
		query.p_desc = p_desc
		query.p_quantity = p_quantity
		if p_image is not None:
			query.p_image = p_image
		query.save()
		return redirect(f'/panel/edititem/{key}')
	return render(request,'edititem.html',{'p':p,'bags':bags,'laptops':laptops,'jewellary':jewellary})

def view_products(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			p = products.objects.all()
			return render(request,'estore/view_products.html',{'products':p})
		else:
			messages.warning(request, 'Not an Admin')
			return redirect('/panel/login')
	else:
			messages.warning(request, 'Not Sign-In')
			return redirect('/panel/login')


def del_c_items(request,key):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			i = request.session['cat']
			delq = recommendation.objects.filter(p_name = key, cluster=i).first()
			delq.delete()
			return redirect(f'/panel/viewcategoryitems/{i}')

def delvoucher(request,key):
	i = request.session['cat']
	delq = vouchers.objects.filter(voucher = key,category = i)
	delq.delete()
	return redirect(f'/panel/addvouchers/{i}')

def add_products(request):
	user = request.user
	if user.is_authenticated:
		if request.session.get('id',None) == "Employee":
			bags = ['Laptop Bags','Purses','Hiking Bags']
			jewellary = ['Rings','Earings','Pendants']
			laptops = ['HP','Lenovo','Dell']
			if request.method == 'POST':
				p_name = request.POST['pn']
				p_price = request.POST['pp']
				p_desc = request.POST['pd']
				p_cat = request.POST['category']
				p_cat2 = request.POST['cat2']
				p_image = request.FILES['img']
				print(p_cat2)
				query = products(p_name = p_name,p_price=p_price,p_desc=p_desc,p_cat=p_cat,p_cat2=p_cat2,p_image=p_image,p_rattings=0,p_quantity=0)
				query.save()
				return view_products(request)

			return render(request,'estore/addproduct.html',{'bags':bags,'jewellary':jewellary,'laptops':laptops})
		else:
			messages.warning(request, 'Not an Admin')
			return redirect('/panel/login')
	else:
			messages.warning(request, 'Not Sign-In')
			return redirect('/panel/login')

def del_product(request,key):
	q = products.objects.filter(id = key).first()
	q.delete()
	return redirect('/panel/viewproducts')

def del_order(request,key):
	q = orders.objects.filter(id = key).first()
	q.delete()
	return redirect('/panel/')

def delivered(request,pid):
	p = orders.objects.filter(id = pid).first()
	p.delivery_status = "Delivered"
	p.save()
	return redirect('/panel/#orders')

def cust_order(request,pid):
	print(request.user.id)
	user = User.objects.filter(id = pid).first()
	order = orders.objects.filter(u_id = user)
	print(order)
	return render(request,'cust_orders.html',{'order':order})