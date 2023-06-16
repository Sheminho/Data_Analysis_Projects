#!/usr/bin/env python
# coding: utf-8

# # Task 4: Exploratory Data Analysis - Terrorism
# ## Author: Mahmoud Ahmed Shimy
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis (EDA
#    )</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Important note:
# All the conclusions, results, and recommendations are derived according to this dataset which is not considering the World Wars as terrorist acts and did not waste the lives of millions of people.
# ### Dataset Description 
# > I have selected the **Global Terrorism** dataset to investigate it and do some **E**xploratory **D**ata **A**nalysis by exploring the correlations between the varies things on it and find patterns to find out the hot zones of terrorism and get all security issues and insights I can derive by answering some question that we will ask now.
# 
# 
# #### Question(s) for Analysis
# <ol>
# <li>First step after importing and wrangling the data is to check the Uni-Variate Analysis by getting the top 5 countries, Governates and Regions by number of attacks. and starts <a href="#Q1">here</a></li>
# <li>Also it is important to know the most used types of attacks and targets globally. <a href="#Q2">here</a></li>
# <li>Going to Bi-Variate analysis it's important to answer some questions like what is the most countries, regions has kills and kills per attack and the most target, attack type in each zone. <a href="#Q3">here</a></li>
# <li>Finally with Multi-Variate Analysis we need to know the most target and attack type in each country in the Region and starts <a href="#Q4">here</a></li>
# </ol>

# ### importing Liberaries and DataFrame
# >This section is to import the necessary liberaries and DataFrame

# In[1]:


# for data frames
import pandas as pd
# for numerical fn.
import numpy as np
# for data visualization
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import datetime as dt
from pandas_profiling import ProfileReport


# In[2]:


# pip install ipywidgets
# pip install pandas-profiling


# <a id='wrangling'></a>
# ## Data Wrangling section
# > In this section we will do some gathering, assessing and cleaning to the data to be more suatable and easy to analyse

# In[3]:


df = pd.read_csv("globalterrorismdb_0718dist.csv", encoding='latin-1')


# In[4]:


df.shape


# Now we know that the data has about 180k observations and 135 column.
# 
# Lets look at 3 random observations.

# In[5]:


# to see all columns
pd.set_option('display.max_columns', None)
df.sample(3)


# 
# ### Data Assessing & Cleaning
# > After gathering the data it has some problems and needs to be cleand so let's take a look on some of these problems.
# 
# Firstly there's many columns that we will not use lets take what we need from columns.

# In[6]:


df = df[["eventid","iday", "iyear", "imonth", "country_txt", "region_txt", "provstate", "city", "latitude", "longitude", "success", "attacktype1_txt","nkill", "target1"]]


# In[7]:


df.shape


# Now it has 15 columns

# In[8]:


df.info()


# In[9]:


df[df.city == "Unknown"].sample(2)


# I've noticed that there's many Unknown cities<br>
# lets make it null values

# In[10]:


df.replace("Unknown", np.nan, inplace=True)


# In[11]:


df[df.iday == 0].sample(2)


# There's many days and months is 0 <br>
# let's make it Null

# In[12]:


df[["iday", "imonth"]] = df[["iday", "imonth"]].replace(0, np.nan)


# In[13]:


df.info()


# In[14]:


df.dropna(inplace=True)


# In[15]:


df.duplicated().sum()


# In[16]:


df.drop_duplicates(inplace=True)


# In[17]:


df.sample(2)


# Now lets creat a new columns calles date 

# In[18]:


df["date"] = pd.to_datetime(dict(year = df.iyear, month = df.imonth, day = df.iday))


# Also lets make the 'eventid' as index for our data then drop it.

# In[19]:


df.set_index(df.eventid, inplace=True)
df.sample()


# In[20]:


df.eventid.duplicated().sum()


# In[21]:


df.drop(columns="eventid",inplace=True)


# As a final step in cleaning data lets rename all columns to be easier to read.

# In[22]:


df.rename(columns={"iday" : "day", "iyear" : "year", "imonth" : "month", "region_txt" : "region", "provstate" : "state", "attacktype1_txt" : "attack_type", "target1" : "target", "country_txt" : "country"}, inplace=True)


# In[23]:


df.head(3)


# In[24]:


df.day = df.day.astype(int)
df.month = df.month.astype(int)
df.nkill = df.nkill.astype(int)


# In[25]:


df.info()


# In[26]:


df.describe()


# Now we have cleaned data without missing or duplicated values and ready to be explored

# <a id='eda'></a>
# ## Exploring Data Section (EDA)
# > After wrangling the data, In this section we will answer some questions by analysing the data to create some Conclusions about the dataframe.
# > All these questions is from my deep mind and of course you may have different questions so don't be restricted by this questions.

# In[27]:


ProfileReport(df)


# In[28]:


df.sample(2)


# <a id='Q1'></a>
# ## Uni-variate analysis

# In[29]:


def pltbar(datax, datay, namex, namey, title):
    plt.bar(
    x = datax,
    height = datay
    )
    plt.xlabel(namex, fontsize = 15)
    plt.ylabel(namey, fontsize = 15)
    plt.title(title, fontsize = 15)


# In[30]:


# City
print("Top 5 countries\n",df.country.value_counts()[:5])


# In[31]:


pltbar(df.country.value_counts()[:5].index, df.country.value_counts()[:5].values, "Country", "# Terrorism act", "Top 5 Countries")


# In[32]:


# State
print("Top 5 Governates\n",df.state.value_counts()[:5])
pltbar(df.state.value_counts()[:5].index, df.state.value_counts()[:5].values, "Governate", "# Terrorism act", "Top 5 Governates")
plt.xticks(rotation = 45);


# In[33]:


# Region
print("Top 5 Regions\n",df["region"].value_counts()[:5])
pltbar(df.region.value_counts()[:5].index, df.region.value_counts()[:5].values, "Region", "# Terrorism act", "Top 5 Regions")
plt.xticks(rotation = 45);


# <a id='Q2'></a>

# In[34]:


# type
print("Top 5 Type of attacks\n",df.attack_type.value_counts()[:5])
pltbar(df.attack_type.value_counts()[:5].index, df.attack_type.value_counts()[:5].values, "Type", "# Terrorism act", "Top 5 Type of attacks")
plt.xticks(rotation = 45);


# In[35]:


# target
print("Top 5 Targets\n",df.target.value_counts()[:5])
pltbar(df.target.value_counts()[:5].index, df.target.value_counts()[:5].values, "Target", "# Terrorism act", "Top 5 Targets")


# In[36]:


# success
plt.pie(df.groupby(df.success).count().day, labels=["Failed", "Succeeded"], autopct='%.2f%%',
       wedgeprops={'linewidth': 2.0, 'edgecolor': 'white'},
       textprops={'size': 'x-large'});
plt.title('Attack Success', fontsize=18)
df.groupby(df.success).count().day


# In[37]:


# Year
df.year.value_counts()[:5]


# In[38]:


# Numerical Data
df.describe()


# <a id='Q3'></a>
# ## Bi-Variate Analysis
# Q1: what is the most country has kills?

# In[39]:


pltbar(df.groupby(df.country).sum().sort_values(by="nkill", ascending=False)[:5].nkill.index,  df.groupby(df.country).sum().sort_values(by="nkill", ascending=False)[:5].nkill.values, "Country", "#of kills", "Top 5 countries has kills")
df.groupby(df.country).sum().sort_values(by="nkill", ascending=False)[:5].nkill


# Q2: What is the top 5 countries in average kills by attack?

# In[40]:


pltbar(df.groupby(df.country).mean().sort_values("nkill", ascending=False)[1:6].index, df.groupby(df.country).mean().sort_values("nkill", ascending=False).nkill[1:6].values, "Country", "Average kills by attack", "Top 5 countries in average kills by attack")
df.groupby(df.country).mean().sort_values("nkill", ascending=False)[:6]


# Q3: What is the most target in each country?

# In[41]:


for x in df.groupby(df.country).sum().sort_values(by="country").index:
    print("The most target in",x,"is",df[df.country == x].groupby("target").count().sort_values('nkill',ascending = False)[:1].index[0],"with",df[df.country == x].groupby("target").count().sort_values('nkill',ascending = False)[:1].day.values,"attacks")


# Q4: What is the most attack_type in each country?

# In[42]:


for x in df.groupby(df.country).sum().sort_values(by="country").index:
    print("The most attack_type in",x,"is",df[df.country == x].groupby("attack_type").count().sort_values('nkill',ascending = False)[:1].index[0],"with",df[df.country == x].groupby("target").count().sort_values('nkill',ascending = False)[:1].day.values,"attacks")


# Q5: what is the most Region has kills?

# In[43]:


pltbar(df.groupby(df.region).sum().sort_values(by="nkill", ascending=False)[:5].nkill.index,  df.groupby(df.region).sum().sort_values(by="nkill", ascending=False)[:5].nkill.values, "Region", "#of kills", "Top 5 Regions has kills")
plt.xticks(rotation = 45);
df.groupby(df.region).sum().sort_values(by="nkill", ascending=False)[:5].nkill


# Q6: What is the top 5 Regions in average kills by attack?

# In[44]:


pltbar(df.groupby(df.region).mean().sort_values("nkill", ascending=False)[:5].index, df.groupby(df.region).mean().sort_values("nkill", ascending=False).nkill[:5].values, "Region", "Average kills by attack", "Top 5 Regions in average kills by attack")
plt.xticks(rotation = 45);
df.groupby(df.region).mean().sort_values("nkill", ascending=False)[:5].nkill


# Q7: What is the most target in each Region?

# In[45]:


for x in df.groupby(df.region).sum().sort_values(by="region").index:
    print("The most target in",x,"is",df[df.region == x].groupby("target").count().sort_values('nkill',ascending = False)[:1].index[0],"with",df[df.region == x].groupby("target").count().sort_values('nkill',ascending = False)[:1].day.values,"attacks")


# Q8: What is the most attack_type in each Region?

# In[46]:


for x in df.groupby(df.region).sum().sort_values(by="region").index:
    print("The most attack_type in",x,"is",df[df.region == x].groupby("attack_type").count().sort_values('nkill',ascending = False)[:1].index[0],"with",df[df.region == x].groupby("target").count().sort_values('nkill',ascending = False)[:1].day.values,"attacks")


# <a id='Q4'></a>
# # Multi-Variate Analysis
# Q9: What is the top 5 states & cities in **Iraq** has #of kills?

# In[47]:


df[df.country == "Iraq"].groupby("state").sum().nkill.sort_values(ascending = False)[:5]


# In[48]:


df[df.country == "Iraq"].groupby("city").sum().nkill.sort_values(ascending = False)[:5]


# Q10: What is the most target & attack_type in **Middle East** countries?

# In[49]:


for x in df[df.region == "Middle East & North Africa"].groupby(df.country).sum().sort_values(by="nkill", ascending = False).index:
    print("The most target in",x,"is",df[df.country == x].groupby("target").count().sort_values('nkill',ascending = False)[:1].index[0],"with",df[df.country == x].groupby("target").count().sort_values('nkill',ascending = False)[:1].nkill.values,"attacks")


# In[50]:


for x in df[df.region == "Middle East & North Africa"].groupby(df.country).count().sort_values(by="day", ascending = False).index:
    print("The most attack_type in",x,"is",df[df.country == x].groupby("attack_type").count().sort_values('nkill',ascending = False)[:1].index[0],"with",df[df.country == x].groupby("attack_type").count().sort_values('nkill',ascending = False)[:1].day.values,"attacks")


# Q11: What is the most target & attack_type in **Iraq** states?

# In[51]:


for x in df[df.country == "Iraq"].groupby(df.state).count().sort_values(by="day", ascending = False).index:
    print("The most target in",x,"is",df[df.state == x].groupby("target").count().sort_values('nkill',ascending = False)[:1].index[0],"with",df[df.state == x].groupby("target").count().sort_values('nkill',ascending = False)[:1].day.values,"attacks")


# In[52]:


for x in df[df.country == "Iraq"].groupby(df.state).count().sort_values(by="day", ascending = False).index:
    print("The most attack_type in",x,"is",df[df.state == x].groupby("attack_type").count().sort_values('nkill',ascending = False)[:1].index[0],"with",df[df.state == x].groupby("attack_type").count().sort_values('nkill',ascending = False)[:1].day.values,"attacks")


# In[53]:


df.to_csv("Modified")


# <a id='conclusions'></a>
# ## Conclusions:
# ### After investigating the data frame we knew the following:
# > - The most Region has terrorism attacks and killed people in the world is **Middle East & North Africa** with $41296$ attacks and $115913$ peoples killed by terrorists.<br>
# > - The most Country has terrorism attacks and killed people in the Middle East and the World is **Iraq** with $21066$ attacks and $68408$ peoples killed by terrorists.<br>
# > - The most Governate has terrorism attacks in Iraq and the World is **Baghdad** with $7129$ attacks.<br>
# > - The most Weapons used in the attacks is **Bombing/Explosion** with $74250$ attacks using this weapon.<br>
# > - The most Targets by Terrorists is **Civilians** with $5688$ attacks on it.<br>
# > - The most country has #of kills per attack is **Barbados** with an average $25$ kills per attack.<br>
# > - The most Region has #of kills per attack is **Sub-Saharan Africa** with an average $4.7$ kills per attack.<br>
# >
# > **Recommendation:**<br>
# > Finally, Iraq faced a fatal war caused by the USA, which caused immense suffering and had far-reaching consequences for the lives of its people. The country's infrastructure has been severely damaged. Despite these challenges, the people of Iraq have shown remarkable resilience, and determination in the face of adversity and terrorism. Ultimately, it is only through cooperation and dialogue that a lasting solution can be found to end the suffering caused by this devastating war.<br>
# ## Data Limitation
# > As I said before the dataset is not considering the World Wars as terrorist acts and did not waste the lives of millions of people in the other hand it considers the war in Iraq as a terrorist act, which is very confusing for me actually.
