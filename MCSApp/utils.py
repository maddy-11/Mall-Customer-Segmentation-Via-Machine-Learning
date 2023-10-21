import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
from .models import *

# d = pd.read_csv("C:/Users/PAK/Desktop/Mall_Customers.csv")

def get_graph():
	buffer = BytesIO()
	plt.savefig(buffer, format = 'png')
	buffer.seek(0)
	image_png = buffer.getvalue()
	graph = base64.b64encode(image_png)
	graph = graph.decode('utf-8')

	graph1 = base64.b64encode(image_png)
	graph1 = graph1.decode('utf-8')
	
	buffer.close()
	return graph

def get_elbow():
	data = fetch_data()
	df = data['d']

	X = df.iloc[:,[4,5]]
	print(X)
	wcss = []
	for i in range(1,11):
		kmeans = KMeans(n_clusters=i,init='k-means++',random_state=0)
		kmeans.fit(X)
		wcss.append(kmeans.inertia_)

	plt.figure(figsize=(12,5))
	plt.plot(range(1,11),wcss , c="cyan")
	plt.title('Elbow Method')
	plt.xlabel('Number of Clusters')
	plt.ylabel('WCSS')

	graph = get_graph()
	return graph

def get_cluster_plot():
	data = fetch_data()
	d = data['d']
	km = data['km']
	cluster1 = d[d.cluster == 0]
	cluster2 = d[d.cluster == 1]
	cluster3 = d[d.cluster == 2]
	cluster4 = d[d.cluster == 3]
	cluster5 = d[d.cluster == 4]
	plt.switch_backend('AGG')
	plt.figure(figsize=(12,5))
	plt.title('Mall Customer Segments')
	plt.scatter(cluster1['income'],cluster1['spending_s'],color = "green", label = 'C1')
	plt.scatter(cluster2['income'],cluster2['spending_s'],color = "grey", label = 'C2')
	plt.scatter(cluster3['income'],cluster3['spending_s'],color = "blue", label = 'C3')
	plt.scatter(cluster4['income'],cluster4['spending_s'],color = "orange", label = 'C4')
	plt.scatter(cluster5['income'],cluster5['spending_s'],color = "red", label = 'C5')
	plt.scatter(km.cluster_centers_[:,1],km.cluster_centers_[:,0], s=100,  c = 'black',label = 'centroids')
	plt.xlabel('Income')
	plt.ylabel('Spending Score (1-100)')

	plt.legend()
	# plt.show()
	
	graph = get_graph()
	return graph

def get_income_plot():
	data = fetch_data()
	d = data['d']

	income_1_20 = d[(d['income']>=1)&(d['income']<=20)]
	income_21_40 = d[(d['income']>=21)&(d['income']<=40)]
	income_41_60 = d[(d['income'] >=41) & (d['income'] <=60)]
	income_61_80 = d[(d['income'] >=61) & (d['income'] <=80)]
	income_81_100 = d[(d['income'] >=81) & (d['income'] <=100)]
	income_101_120 = d[(d['income'] >=101) & (d['income'] <=120)]
	income_120_above = d[(d['income'] >=120) ]


	age_x = ['1-20','21-40','41-60','61-80','81-100','100-120','120+']
	age_y = [len(income_1_20.values),len(income_21_40.values),len(income_41_60.values),len(income_61_80.values),len(income_81_100.values),len(income_101_120.values),len(income_120_above.values)]

	plt.figure(figsize=(12,6))
	plt.title('Annual Income')
	sns.barplot(x=age_x,y=age_y,palette='hsv')
	plt.xlabel('Annual Income')
	plt.ylabel('Numer of Customers')

	graph = get_graph()
	return graph

def get_spending_score():
	data = fetch_data()
	d = data['d']

	score_1_20 = d[(d['spending_s']>=1)&(d['spending_s']<=20)]
	score_21_40 = d[(d['spending_s']>=21)&(d['spending_s']<=40)]
	score_41_60 = d[(d['spending_s'] >=41) & (d['spending_s'] <=60)]
	score_61_80 = d[(d['spending_s'] >=61) & (d['spending_s'] <=80)]
	score_81_100 = d[(d['spending_s'] >=81) & (d['spending_s'] <=100)]


	age_x = ['1-20','21-40','41-60','61-80','81-100']
	age_y = [len(score_1_20.values),len(score_21_40.values),len(score_41_60.values),len(score_61_80.values),len(score_81_100.values)]

	plt.figure(figsize=(12,6))
	plt.title('Most Spending Score')
	sns.barplot(x=age_x,y=age_y,palette='bright')
	plt.xlabel('Spending Score')
	plt.ylabel('Numer of Customers')

	graph = get_graph()
	return graph

def genders():
	data = fetch_data()
	d = data['d']

	female = d[(d.gender=='Female')]
	male = d[d.gender == 'Male']
	gender = [f'Males = {len(male.values)}',f'Female = {len(female.values)}']
	number = [len(male.values),len(female.values)]

	plt.figure(figsize=(12,6))
	plt.title('Gender Plot')
	sns.barplot(x=gender,y=number,palette='bright')
	plt.xlabel('Gender')
	plt.ylabel('Number of Customers')
	graph = get_graph()
	return graph

def customers():
	df = dataset.objects.values()
	d = pd.DataFrame.from_records(df)
	plt.figure(figsize=(12,6))
	plt.title('Rough Data')
	plt.scatter(d['income'],d['spending_s'])
	plt.xlabel("Income")
	plt.ylabel("Spending Score")
	graph = get_graph()
	return graph

def get_clusters():
	r = dataset.objects.all()
	r.delete()
	d = pd.read_csv("C:/Users/PAK/Desktop/Mall_Customers.csv")
	km = KMeans(n_clusters = 5, init = 'k-means++',random_state=0)
	y = km.fit_predict(d[['Spending Score (1-100)','Annual Income (k$)']])
	d['cluster'] = y
	for index, row in d.iterrows():
		dataset.objects.create(
			cust_id=row['CustomerID'],
			gender=row['Gender'],
			age=row['Age'],
			income=row['Annual Income (k$)'],
			spending_s=row['Spending Score (1-100)'],
			cluster=row['cluster']
		)

def fetch_data():
	df = dataset.objects.values()
	x = pd.DataFrame.from_records(df)
	x = x.drop(columns=['cluster'])
	km = KMeans(n_clusters = 5, init = 'k-means++',random_state=0)
	y = km.fit_predict(x[['income','spending_s']])
	x['cluster'] = y
	return {'d':x,'km':km}
	

	
def fetch_clusters(num):
	n = int(num)
	data = dataset.objects.values()
	x = pd.DataFrame.from_records(data)
	km = KMeans(n_clusters = 5, init = 'k-means++',random_state=0)
	y = km.fit_predict(x[['spending_s','income']])
	x['cluster'] = y
	c = x.loc[x['cust_id'] == n]
	d = c.iloc[-1]
	d = d.iloc[-1]
	return d
	