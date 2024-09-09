#!/usr/bin/env python
# coding: utf-8

# In[221]:


import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt # plot graphs
import seaborn as sns # plot graphs
from scipy import stats
import warnings
warnings.filterwarnings('ignore')


# In[222]:


walmart_data=pd.read_csv("walmart-sales-dataset-of-45stores.csv")#read of data set
walmart_data #display


# In[223]:


walmart_data.head(10)# display first 10 raw


# In[224]:


walmart_data.tail(10) #display  last 10 raw


# In[225]:


walmart_data.sample(10) #display 10 random raw


# In[226]:


walmart_data.info() # information about each col


# In[227]:


walmart_data.describe(include='all') # describe all data


# In[228]:


walmart_data.describe(include='number')# describe all numeric data


# In[229]:


walmart_data.describe(include='object') # describe all non numeric data


# In[230]:


# print all histogram (show ferquency of element in cols without remove outlieurs)
plt.figure(figsize=(30, 20))

plt.subplot(2, 3, 1)
plt.hist(walmart_data['Weekly_Sales'], bins=20, color='lightgreen', edgecolor='green')
plt.xlabel('Weekly_Sales')
plt.ylabel('Frequency')
plt.title('Distribution of Weekly_Sales')

plt.subplot(2, 3, 2)
plt.hist(walmart_data['Temperature'], bins=20, color='purple', edgecolor='white')
plt.xlabel('Temperature')
plt.ylabel('Frequency')
plt.title('Distribution of Temperature')

plt.subplot(2, 3, 3)
plt.hist(walmart_data['Fuel_Price'], bins=20, color='pink', edgecolor='red')
plt.xlabel('Fuel_Price')
plt.ylabel('Frequency')
plt.title('Distribution of Fuel_Price')

plt.subplot(2, 3, 4)
plt.hist(walmart_data['Unemployment'], bins=20, color='yellow', edgecolor='black')
plt.xlabel('Unemployment')
plt.ylabel('Frequency')
plt.title('Distribution of Unemployment')

plt.subplot(2, 3, 5)
plt.hist(walmart_data['CPI'], bins=20, color='darkorange', edgecolor='gold')
plt.xlabel('CPI')
plt.ylabel('Frequency')
plt.title('Distribution of CPI')

plt.tight_layout()
plt.show()


# In[231]:


walmart_data.isnull()#show each col. contain null (true or false)


# In[232]:


walmart_data.isnull().sum()# display null in each col.


# In[233]:


walmart_data.dropna(inplace=True)#remove null


# In[234]:


walmart_data.duplicated()#show dublicate


# In[235]:


walmart_data.duplicated().sum()# display dublicate in each col.


# In[236]:


# Q1
max_sales_store = walmart_data.groupby('Store')['Weekly_Sales'].sum().round().sort_values(ascending=False) # هترتب القيم تنازلى
#sum عشان يجمع القيم - round هتقرب لرقم صحيح -groupby...used to group data on common values 
pd.DataFrame(max_sales_store).head()# display 5 first raw


# In[237]:


max_sales=max_sales_store.idxmax()#display top value
max_sales


# In[238]:


# Q2
max_standard_deviation =walmart_data.groupby('Store')['Weekly_Sales'].std().round().sort_values(ascending=False)
pd.DataFrame(max_standard_deviation).head()#std=calculate standard deviation


# In[239]:


sd_sales=max_standard_deviation.idxmax()#display top value
sd_sales


# In[240]:


# Q3
nonHoliday_mean_sales = walmart_data[walmart_data['Holiday_Flag'] == 0]['Weekly_Sales'].mean().round()#هنا بيتعامل فى حاله مفيش اجازه 
nonHoliday_mean_sales# mean= calculate expected values 


# In[241]:


# Find holidays that have higher sales than the mean sales in the non-holiday season for all stores 
non_holiday_mean_sales = walmart_data[walmart_data['Holiday_Flag'] == 0]['Weekly_Sales'].mean()
high_sales_holidays = walmart_data[(walmart_data['Holiday_Flag'] == 1) & (walmart_data['Weekly_Sales'] > non_holiday_mean_sales)]
print("Holidays with higher sales than mean sales in non-holiday season:")
print(high_sales_holidays[['Date', 'Weekly_Sales']])


# In[242]:


#inconsistency
walmart_data['Date'] = pd.to_datetime(walmart_data['Date'], format='%d-%m-%Y')# عشان اوحد شغل الفورمات بتاعت ال date
walmart_data


# In[243]:


#Holiday Events
Super_Bowl=['2010-02-12', '2011-02-11', '2012-02-10']
Labour_Day=['2010-09-10', '2011-09-09', '2012-09-07']
Thanksgiving=['2010-11-26', '2011-11-25']
Christmas=['2010-12-31', '2011-12-30']

#check values true or false 
# Calculate holiday events sales
Super_Bowl_sales = walmart_data. loc[walmart_data.Date.isin(Super_Bowl) ] ['Weekly_Sales' ].mean( )
Labour_Day_sales = walmart_data. loc[walmart_data.Date.isin(Labour_Day) ]['Weekly_Sales' ] .mean() 
Thanksgiving_sales = walmart_data. loc[walmart_data.Date. isin(Thanksgiving) ] [ 'Weekly_Sales' ] .mean( )
Christmas_sales = walmart_data. loc[walmart_data. Date.isin(Christmas) ] ['Weekly_Sales'].mean()
print(Super_Bowl_sales , Labour_Day_sales , Thanksgiving_sales , Christmas_sales)


# In[244]:


merge=pd.DataFrame([{'Super_Bowl_sales':Super_Bowl_sales,
                  'Labour_Day_sales':Labour_Day_sales,
                 'Thanksgiving_sales':Thanksgiving_sales, 
                 'Christmas_sales':Christmas_sales}]).T


# In[245]:


result=merge.idxmax()#display top value
result


# In[246]:


holidays = ['Super Bowl', 'Labour Day', 'Thanksgiving', 'Christmas', 'non_holiday']
mean_sales = [Super_Bowl_sales, Labour_Day_sales, Thanksgiving_sales, Christmas_sales , nonHoliday_mean_sales]
# Plotting
plt.figure(figsize=(8, 6))
plt.bar(holidays, mean_sales, color=['green', 'yellow', 'darkblue', 'red','orange'])
plt.title('Mean Weekly Sales for Different Holidays')
plt.xlabel('Holiday')
plt.ylabel('Mean Weekly Sales')
plt.show()


# In[247]:


# Q4 # December is first  the maximum sales among the other months.
# November is second (it include the thankGiving holidays which impact on the sales possitively)
# february is third 
# April is fourth
# May,June and july is fifth 
walmart_data['Month'] = walmart_data['Date'].dt.month #هنا هيقسم التاريخ وياخد منه جزء الشهور ويعبيه فى عمود جديد
walmart_data['Month']


# In[248]:


monthly_sales = walmart_data.groupby('Month')['Weekly_Sales'].sum()
print(monthly_sales) 


# In[249]:


for x in walmart_data.index:# هنا هيقسم السنه لجزئين متساويين وهيعمل عمود جديد ليهم 
    if walmart_data.loc[x,"Month"] <= 6:
        walmart_data.loc[x,"Semester"] = 'First'
    else:
        walmart_data.loc[x,"Semester"] = 'Second'


# In[250]:


monthly_sales = walmart_data.groupby('Semester')['Weekly_Sales'].sum()
print(monthly_sales) 


# In[251]:


plt.figure(figsize=(15, 6))
#bar plot of view months and semesters
plt.subplot(1, 2, 1)
plt.bar(walmart_data['Month'], walmart_data['Weekly_Sales'], color='darkviolet')# semester two is more than from semester one
plt.xlabel('Months')
plt.ylabel('Weekly_Sales')
plt.title('Monthly Sales')

plt.subplot(1, 2, 2)
plt.bar(walmart_data['Semester'], walmart_data['Weekly_Sales'], color='lightgreen')
plt.xlabel('Semester')
plt.ylabel('Weekly_Sales')
plt.title('Semester Sales')
plt.show()


# In[252]:


walmart_data #display data_set


# In[253]:


# for all graphs ( weak_correlation)
# positive_weak_correlation (Fuel_Price ) 
# negative_weak_correlation (Temperature - Unemployment  - CPI) 


# In[254]:


sns.scatterplot(data=walmart_data, x='Temperature', y='Weekly_Sales', color='yellow')
sns.regplot(data=walmart_data, x='Temperature', y='Weekly_Sales', scatter=False, color='Black')
plt.xlabel('Temperature')
plt.ylabel('Weekly Sales')
plt.title('Weekly Sales vs Temperature')


# In[255]:


temperature = np.array(walmart_data['Temperature'])
weekly_sales = np.array(walmart_data['Weekly_Sales'])
correlation_coef = np.corrcoef(temperature, weekly_sales)[0, 1]
print("correlation_coef: ", correlation_coef )


# In[256]:


sns.scatterplot(data=walmart_data, x='Fuel_Price', y='Weekly_Sales', color='green')
sns.regplot(data=walmart_data, x='Fuel_Price', y='Weekly_Sales', scatter=False, color='Black')
plt.xlabel('Fuel_Price')
plt.ylabel('Weekly Sales')
plt.title('Weekly Sales vs Fuel_Price')


# In[257]:


Fuel_Price = np.array(walmart_data['Fuel_Price'])
weekly_sales = np.array(walmart_data['Weekly_Sales'])
correlation_coef = np.corrcoef(Fuel_Price, weekly_sales)[0, 1]
print("correlation_coef: ", correlation_coef )


# In[258]:


sns.scatterplot(data=walmart_data, x='Unemployment', y='Weekly_Sales', color='red')
sns.regplot(data=walmart_data, x='Unemployment', y='Weekly_Sales', scatter=False, color='Black')
plt.xlabel('Unemployment')
plt.ylabel('Weekly Sales')
plt.title('Weekly Sales vs Unemployment')


# In[259]:


Unemployment = np.array(walmart_data['Unemployment'])
weekly_sales = np.array(walmart_data['Weekly_Sales'])
correlation_coef = np.corrcoef(Unemployment, weekly_sales)[0, 1]
print("correlation_coef: ", correlation_coef )


# In[260]:


sns.scatterplot(data=walmart_data, x='CPI', y='Weekly_Sales', color='purple')
sns.regplot(data=walmart_data, x='CPI', y='Weekly_Sales', scatter=False, color='Pink')
plt.xlabel('CPI')
plt.ylabel('Weekly Sales')
plt.title('Weekly Sales vs CPI')


# In[261]:


CPI = np.array(walmart_data['CPI'])
weekly_sales = np.array(walmart_data['Weekly_Sales'])
correlation_coef = np.corrcoef(CPI, weekly_sales)[0, 1]
print("correlation_coef: ", correlation_coef )

