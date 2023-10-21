from django.shortcuts import render,redirect
from django.contrib.auth import logout,login,authenticate
from django.contrib import messages
from django.db.models import Sum
from .models import *
from MCSApp.models import *
from MCSApp.utils import fetch_clusters
from .forms import *
import math
# Create your views here.
boolean= False

def home(request):
	return render(request,'estore/homepage.html')

def cart(request):
	request.session['p_n'] = None
	discount = 0
	request.session['discount']=0
	context = orders.objects.filter(u_id = request.user,delivery_status='Order Pending')
	orders_ = orders.objects.filter(u_id = request.user,delivery_status='Order Pending')
	t_sum = orders_.aggregate(Sum('t_amount'))
	t_amount = t_sum['t_amount__sum']
	f_price = t_amount
	if f_price is None:
		f_price = 0
	request.session['t_amount'] = f_price
	if request.method == 'POST':
		v = request.POST['coupon_']
		voucher = vouchers.objects.filter(voucher=v).first()
		if voucher:
			p_age = voucher.percentage
# looking if voucher works for the specific category of the customer
			v_cat = int(voucher.category)
			user = request.user
			cust = customer.objects.filter(user = user).first()
			cluster = int(cust.c_data.cluster)
			if v_cat == cluster:
				discount = (p_age/100)*t_amount
				request.session['discount'] = discount
				print(request.session['discount'])
				f_price = t_amount - discount
				request.session['t_amount'] = f_price
			else:
				print("here")
		else:
			pass
	return render(request,'estore/cart.html',{'context':context,'sum':request.session['t_amount'],'f_price':f_price,'d':discount})

def checkout(request):

	print(fetch_clusters('201'))
	if request.method == 'POST':
		user = request.user
		cust = customer.objects.filter(user = user).first()
		s_score = cust.c_data.spending_s
		f_amount = request.session.get('t_amount',None)
		print(s_score)
		# -------------------------------
		address = request.POST['add']
		city = request.POST['city']
		province = request.POST['province']
		phone = request.POST['phone']
		c_number = request.POST['card_number']
		c_name = request.POST['card_name']
		exp_month = request.POST['exp_month']
		exp_year = request.POST['exp_year']
		card_cvv = request.POST['cvv']
		# -------------------------------
		card_auth = card.objects.filter(c_num = c_number,c_name=c_name,c_month=exp_month,c_year=exp_year,cvv=card_cvv).first()
		if card_auth is None:
			# delivery address
			d_add = d_address(address=address,city=city,province=province,phone=phone)
			# d_add.save()

			# spending-score calculation
			if s_score >= 0 and s_score <= 20:
				s_score = math.floor(s_score + (f_amount/10))
				cust.c_data.spending_s = s_score
				cust.c_data.save()
			elif s_score > 20 and s_score <= 30:
				s_score = math.floor(s_score + (f_amount/12.5))
				cust.c_data.spending_s = s_score
				cust.c_data.save()
			elif s_score >= 31 and s_score <= 40:
				s_score = math.floor(s_score + (f_amount/15))
				cust.c_data.spending_s = s_score
				cust.c_data.save()
			elif s_score >= 41 and s_score <= 50:
				s_score = math.floor(s_score + (f_amount/17.5))
				cust.c_data.spending_s = s_score
				cust.c_data.save()
			elif s_score >= 51 and s_score <= 60:
				s_score = math.floor(s_score + (f_amount/20))
				cust.c_data.spending_s = s_score
				cust.c_data.save()
			elif s_score >= 61 and s_score <= 70:
				s_score = math.floor(s_score + (f_amount/15))
				cust.c_data.spending_s = s_score
				cust.c_data.save()
			elif s_score >= 71 and s_score <= 80:
				s_score = math.floor(s_score + (f_amount/22.5))
				cust.c_data.spending_s = s_score
				cust.c_data.save()
			elif s_score >= 81 and s_score <= 90:
				s_score = math.floor(s_score + (f_amount/25))
				cust.c_data.spending_s = s_score
				cust.c_data.save()
			elif s_score >= 91 and s_score < 100:
				s_score = math.floor(s_score + (f_amount/27.5))
				cust.c_data.spending_s = s_score
				cust.c_data.save()

			o = orders.objects.filter(u_id=user,delivery_status='Order Pending')
			for i in o:
				i.delivery_status = 'Out For Delivery'
				i.save()
			cluster = fetch_clusters(201)
			cust.c_data.cluster = cluster
			cust.c_data.save()
			return redirect('/store/invoice')
		else:
			print('Card Declined')
		
	return render(request,'estore/checkout.html')

def bill(request):
	
	total = 0
	total = request.session.get('t_amount',0)
	user = request.user
	bill = orders.objects.filter(u_id=user,delivery_status='Out For Delivery')
	if request.method == 'POST':
		for i in bill:
			i.delivery_status = 'To be Delivered'
			i.save()
		return redirect('/store/recommended/')
	return render(request,'estore/bill.html',{'price':total,'orders':bill,'dis':request.session.get('discount',None)})

def buy_product(request,pd):
	user = request.user
	p = products.objects.filter(id = pd).first()
	if request.method == 'POST':
		pn = request.session.get('p_n',None)
		if pn is None:
			pn = 0
		request.session['p_n'] = pn + 1
		color = request.POST['color']
		quantity = int(request.POST['no_of_items'])
		price = p.p_price
		t_price = price * quantity
		order = orders(p_id=p,u_id=user,color=color,quantity=quantity,price=price,t_amount=t_price,delivery_status='Order Pending')
		order.save()
		p.p_quantity = p.p_quantity - quantity
		p.save()
	r = review.objects.order_by('-id')
	rev = r.filter(p_id = p)
	return render(request,'estore/buy_product.html',{'p':p,'r':rev,'pn':request.session.get('p_n',None)})	

def p_categories(request,cat):
	data = products.objects.filter(p_cat = cat)
	return render(request,'estore/products.html',{'x':data,'cat':cat})



def cust_login(request):
	if request.method == 'POST':
		uname = request.POST['uname']
		pass_ = request.POST['pass']
		user = authenticate(request,username = uname, password=pass_)
		if user is not None:
			login(request, user)
			users = User.objects.get(username=uname)
			value = Account.objects.filter(user = users).first()
			if value is not None:
				request.session['id'] = value.user_role
			return redirect("/")
		else:
			messages.warning(request,"Incorrect Credentials")
			return render(request, 'estore/login.html')
	else:
		return render(request, 'estore/login.html')

def cust_register(request):
	if request.method == 'POST':
		uname = request.POST['uname']
		fname = request.POST['f_name']
		lname = request.POST['l_name']
		email = request.POST['email']
		gender = request.POST['gender']
		age = request.POST['age']
		income = request.POST['income']
		pass_ = request.POST['pass']
		rpass = request.POST['rpass']
		q = User.objects.filter(username=uname).first()
		if not q:
			q = User.objects.filter(email=email).first()

		if q:
			cust = customer.objects.filter(user = q).first()
			if cust:
				messages.warning(request,'User Exists')
				return render(request, 'estore/register.html')
			else:
				y = dataset.objects.all().last()
				y = y.cust_id
				y=y+1

				x = dataset(cust_id = y, gender=gender, age=age, income = income, spending_s= 0, cluster = 0)
				x.save()

				user = User.objects.get(username = uname)
				cdata = dataset.objects.get(cust_id = y)
				c = customer(user=user,c_data=cdata,user_role="Customer")
				c.save()
				messages.success(request,"Account Created")
				return render(request, 'estore/login.html')

		else:
			a = User.objects.create_user(uname,email,pass_)
			a.first_name = fname
			a.last_name = lname
			a.save()

			y = dataset.objects.all().last()
			y = y.cust_id
			y=y+1

			x = dataset(cust_id = y, gender=gender, age=age, income = income, spending_s= 0, cluster = 0)
			x.save()

			user = User.objects.get(username = uname)
			cdata = dataset.objects.get(cust_id = y)
			c = customer(user=user,c_data=cdata,user_role="Customer")
			c.save()
			messages.success(request,"Account Created")
			return render(request, 'estore/login.html')
	else:
		return render(request, 'estore/register.html')


def reviews(request,pid):
	rev = request.POST['review']
	rattings = request.POST['rattings']
	user = request.user
	name = f"{user.first_name} {user.last_name}"
	p_id = products.objects.filter(id = pid).first()
	
	query = review(r_name=name,review=rev,rattings=rattings,p_id=p_id,u_id=user)
	query.save()
	return redirect(f'/store/buy/{pid}/')

def delp(request,pid):
	d_order = orders.objects.filter(id = pid).first()
	p = d_order.p_id
	p.p_quantity = p.p_quantity + 1
	p.save()
	d_order.delete()
	return redirect('/store/cart')

def recommended(request):
	if request.user.is_authenticated:
		user = request.user
		cust = customer.objects.filter(user = user).first()
		cluster = cust.c_data.cluster
		print(cluster)
		a = recommendation.objects.filter(cluster = cluster)
		data = []
		
		for i in a:
			x = products.objects.filter(p_name = i.p_name).first()
			data.append(x)

		return render(request,'estore/recommended.html',{'data':data})
	else:
		return redirect('/store/home')
	
def update_p(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			uname = request.POST['uname']
			fname = request.POST['f_name']
			lname = request.POST['l_name']
			email = request.POST['email']
			gender = request.POST['gender']
			age = request.POST['age']
			income = request.POST['income']
			pass_ = request.POST['pass']
			rpass = request.POST['rpass']

			u = request.user
			u.username = uname
			u.first_name = fname
			u.last_name = lname
			u.email = email
			if pass_ == rpass:
				if pass_ != '':
					u.password = pass_
				c = customer.objects.filter(user = u).first()
				c.c_data.age = age
				c.c_data.gender = gender
				c.c_data.income = income
				c.c_data.save()
				u.save()
			else:
				print('Passwords did not Match')

			return redirect('/store/update')
		user = request.user
		cust = customer.objects.filter(user=user).first()
		return render(request,'estore/updateprofile.html',{'user':user,'c':cust})
	return redirect('/store/login')

def store_notifications(request, pid):
    user = User.objects.filter(id = pid).first()
    q2 = customer.objects.filter(user = user)
    cat = q2.first().c_data.cluster
    query = notifications.objects.filter(category = cat)
    
    return render(request, 'estore/notifications.html', {'data': query})

def invoice(request):
	user = request.user
	total = 0
	total = request.session.get('t_amount',0)
	bill = orders.objects.filter(u_id=user,delivery_status='Out For Delivery')
	if request.method == 'POST':
		for i in bill:
			i.delivery_status = 'To be Delivered'
			i.save()
		return redirect('/store/recommended/')
	return render(request,'estore/invoice.html',{'price':total,'orders':bill,'user':user,'dis':request.session.get('discount',None)})
	
