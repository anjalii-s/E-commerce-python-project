#!/usr/bin/env python
# coding: utf-8

# #                E-COMMERCE SALES ANALYSIS

# #### This project aims to analyse sales of an online store.The raw data is uploaded into python as csv file.Data has 9994 rows and 21 columns.This project uses libraries like pandas,numpy,seaborn,matplotlib and plotly for calculations and visualisations.
# 

# Let's start with importing the libraries and modules...

# In[190]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px 
#Plotly Express is a great library for creating interactive plots in Python
import plotly.graph_objects as go
#Plotly Graph Objects is another powerful library for creating detailed and customizable plots in Python
import plotly.io as pio
#Plotly.iois a versatile library for input/output operations in Plotly
import plotly.colors as colors
#Plotly.colorsis a handy module for working with colors in Plotly
pio.templates.default="plotly_white"
#plotly_white: A clean, white background with gridlines.
#changes the default template for all plots to the "plotly_white" theme


# ### Load data into python with pandas

# In[211]:


data=pd.read_csv('Sample - Superstore.csv',encoding ='latin-1')
#without encoding latin-1,UnicodeDecodeError is observed,since file is not in UTF-8


# In[212]:


data


# ### Get details of all columns of the data

# In[213]:


data.info()


# Therefore, there is no missing values in the data

# ### Get a summary of all data

# In[181]:


data.describe()


#  From above data we get the average profit of sales (mean)as 28.65 dollars,average discount-15%,average sales is around 4 numbers and average sales of the store is around 229 dollars.

# ### Data cleaning

#  We see  Order Date and Ship Date  appears as object.
# We will convert it to date-time

# In[182]:


data['Order Date']=pd.to_datetime(data['Order Date'])
data['Ship Date']=pd.to_datetime(data['Ship Date'])
#check the changes
data[['Order Date','Ship Date']].info() 


# Successfully changed to date time format

# ### Visualise the given data 

# ##### Using seaborn heatmap  and matplotlib 

# The numbers shown in the heatmap represent the correlation coefficients between the variables. A correlation coefficient is a statistical measure that describes the strength and direction of the relationship between two variables. 
# 1:Perfect positive correlation.One variable increases,other also increases,
# -1:Perfect negative.One variable increases,other decreases,
# 0:No correlation.No linear relationship between variables.

# In[202]:


sns.heatmap(data[['Sales','Profit','Quantity','Discount']].corr(),
            annot=True,cmap='Pastel2');
plt.title('Correlation Matrix')


# #### Find out sales by region.Which region has most and least sales ?

# We will plot a pie chart with matplotlib to find the region with maximum and minimum sales.

# In[204]:


Sales_by_region=data.groupby('Region')['Sales'].sum().reset_index()
Sales_by_region.set_index('Region').plot.pie(y='Sales', autopct='%1.1f%%', legend=False)
plt.title('Sales by Region')


# From the above pie chart,it shows West region has highest sales of 31.6% and least sales is for South region with sales of 17.1%.

# ### Monthly sales analysis
# 
# #### Find out which months have the maximum and minimum sales.

# We add new columns month,year,day and extract those ,and group them to visualise and find the results.

# In[207]:


data['Order month']=data['Order Date'].dt.month
data['Order year']=data['Order Date'].dt.year
data['Order Day of week']=data['Order Date'].dt.dayofweek 
# adding new columns to the data,extracting month,year,day.


# In[208]:


data.head(1)


# In[18]:


#group by order month and find sum of sales and reset the index
monthly_sales = data.groupby('Order month')['Sales'].sum().reset_index()
monthly_sales


# #### Data Visualisation of monthly sales

# ##### By matplotlib

# In[19]:


import matplotlib.pyplot as plt
monthly_sales.plot.line(x='Order month',figsize=(5,4))
plt.title('Monthly Sales',fontweight='bold')
plt.ylabel('Sales in Dollars')


# From line graph we see that highest sales occured in November and lowest in February.

# ### Sales by category analysis
# 
# #### Which category of items was sold the least?Also find the %.

# We group by Category ,find sum of sales and plot it in a donut pie chart and get results.

# In[209]:


Sales_by_category=data.groupby('Category')['Sales'].sum().reset_index()
Sales_by_category


# #### Visualising sales by category

# ##### By plotly

# In[21]:


fig=px.pie(Sales_by_category,values ='Sales',names='Category',hole=0.5,
          color_discrete_sequence=px.colors.qualitative.Set2)
#values specify columns to use for values 
#names specify columns to use as names
fig.update_layout(title='Sales by category')
fig.update_traces(textposition='auto',textinfo='percent+label')
#automatically place text in available space and data points
fig.show()


# From the above we see Office supplies had least sales with total percentage of 31.3.

# ### Profit by category analysis
# 
# #### Find the most profit making category.

# Group by category,find sum of profits and visualise.

# In[22]:


profit_by_category=data.groupby('Category')['Profit'].sum().reset_index()
profit_by_category


# #### Visualising profit by category

# ##### By seaborn

# In[23]:


import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(4,3))
plt.title('Profit by category',fontweight='bold')
sns.barplot(x='Category', y='Profit',data=profit_by_category)
plt.show()


# From above bar graph,we see items in Technology category made most profits.

# ### Profit by sub-category
# 
# #### How many items cause a loss to  the company?

# We find profit by subcategory ,grouping items under subcategory and finding sum of profit.Visualise to get desired result.

# In[24]:


profit_by_subcategory=data.groupby('Sub-Category')['Profit'].sum().reset_index()
profit_by_subcategory


# #### Visualisation of profit by sub category

# #### Using plotly

# In[25]:


fig=px.bar(profit_by_subcategory,x='Sub-Category',y='Profit',
           title='Profit by Sub-Category',width=520,height=400)
fig.show()


# Here,we see tables,bookcases and supplies have negative profit.Hence,3 items caused loss to the company.

# ### Visualise sales and profit by customer segment
# 
# Here we use group by and aggregate function to sum up Sales and Profit columns,then plot bar graph using plotly.

# In[137]:


sales_profit_by_custseg=data.groupby('Segment').agg({'Sales':'sum','Profit':'sum'}).reset_index()
sales_profit_by_custseg
color_palette=colors.qualitative.Pastel

fig=go.Figure()#initializes a new Plotly figure
#fig.add_trace(go.Bar(...)): This adds a bar trace to the figure fig.
fig.add_trace(go.Bar(x=sales_profit_by_custseg['Segment'],
                     y=sales_profit_by_custseg['Sales'],
                    name='Sales',
                    marker_color=color_palette[10]))#This sets the color of the bars using the 11th color in the color_palette.


fig.add_trace(go.Bar(x=sales_profit_by_custseg['Segment'],
                     y=sales_profit_by_custseg['Profit'],
                    name='Profit',
                    marker_color=color_palette[6]))
fig.update_layout(title='Sales and profit by customer segment',
                 xaxis_title='Customer Segment',
                 yaxis_title='Amount')


# ### Sales to profit ratio

# Sale to profit ratio can be found by dividing sales by profit 

# In[146]:


import numpy as np
sales_profit_by_custseg=data.groupby('Segment').agg({'Sales':'sum','Profit':'sum'}).reset_index()

sales_profit_by_custseg['Sale_to_profit_ratio'] = np.divide(sales_profit_by_custseg['Sales'], sales_profit_by_custseg['Profit'])

print(sales_profit_by_custseg[['Segment','Sale_to_profit_ratio']])


# We have obtained the sale to profit ratio by segment.

# ### Conclusion 
# 
# With the help of python we were easily able to calculate and plot graphs to find various business sales aspects.From the raw data available ,we were able to calculate and analyse various sales trends.Visualisation provided easy understanding of the data.This can help business in taking future decisions for better growth.
