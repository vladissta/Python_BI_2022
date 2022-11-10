#!/usr/bin/env python
# coding: utf-8

# In[3]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from matplotlib.patches import ConnectionPatch


# ## Working with real data

# ### read_gff and read_bed6 functions for reading the corresponding formats.

# In[2]:


def read_gff(file):
    return pd.read_table(file , sep='\t', skiprows=1, 
                  names = ['chromosome', 'source', "type", "start", "end", "score", "strand", "phase", "attributes"])


# In[3]:


def read_bed6(file):
    return pd.read_table(file, sep='\t', names = ["chromosome", "start", "end", "name", "score", "strand"])


# ### Tables

# In[4]:


gff = read_gff('rrna_annotation.gff')
gff


# In[5]:


bed = read_bed6('alignment.bed')
bed


# ### Renaming attributes column

# In[6]:


gff.attributes = gff.attributes.str.extract(r"([^=]+S )")
gff


# ### 5S, 16S and 23S counting and plotting barplot

# In[7]:


chr_types_rna_count = gff.groupby(['chromosome']).attributes.value_counts().to_frame().rename(columns={'attributes': 'count'}).reset_index()
chr_types_rna_count


# In[8]:


fig, axes = plt.subplots(figsize=(14, 8), tight_layout=True);

sns.barplot(chr_types_rna_count, x = 'chromosome', y = 'count', hue = 'attributes');
plt.xticks(rotation=90);
plt.legend(loc ='upper right', prop={'size': 13}, title = 'RNA type').get_title().set_fontsize('13')
plt.ylabel('Count')
plt.xlabel('Sequence')
plt.tight_layout();


# ### Aligning like in bedtools!

# In[9]:


bed_align = gff.merge(bed, on = 'chromosome', suffixes=('_x', '_y'))
bed_align = bed_align.loc[(bed_align.start_x >= bed_align.start_y) & (bed_align.end_x <= bed_align.end_y)]
bed_align


# ## Plot customization 

# ### Table of genes expression

# In[4]:


de = pd.read_table('diffexpr_data.tsv.gz')
de


# ### Min and Max values of log fold change

# In[5]:


min_x = de.logFC.min()
max_x = de.logFC.max()

min_x, max_x


# ### Creatig new column with annotations of down/up significant/non-significant genes

# **This colum was used for coloring**

# In[6]:


de.loc[(de.logFC > 0) & (de.log_pval > -np.log10(0.05)), 'down_up'] = 'Significantly upregulated'
de.loc[(de.logFC <= 0) & (de.log_pval > -np.log10(0.05)), 'down_up'] = 'Significantly downregulated'
de.loc[(de.logFC > 0) & (de.log_pval <= -np.log10(0.05)), 'down_up'] = 'Non-significantly upregulated'
de.loc[(de.logFC <= 0) & (de.log_pval <= -np.log10(0.05)), 'down_up'] = 'Non-significantly downregulated'

de.down_up.value_counts()


# ### Top 2 up- and downregulated genes

# In[7]:


top_upreg = de.loc[de.down_up == 'Significantly upregulated'].sort_values(by = "logFC", ascending = False).head(2)
top_upreg


# In[8]:


top_downreg = de.loc[de.down_up == 'Significantly downregulated'].sort_values(by = "logFC").head(2)
top_downreg


# In[9]:


genes_to_annotate = pd.concat([top_downreg, top_upreg]).iloc[:,[0,1,4]]
genes_to_annotate


# ### Finally, the plot!

# In[12]:


#parameters for bold italic font of math formulas in latex
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.bf'] = 'Arial:italic:bold' #иначе жирным и курсивным латех у меня не становится...(

# initial plotiing
fig, axes = plt.subplots(figsize=(12, 8), tight_layout=True);

sc = sns.scatterplot(data=de, x='logFC', y="log_pval", hue ="down_up", linewidth=0, s=24,
               palette=['green','darkorange', 'red','steelblue']);

# legend
sc.legend(prop={'size':12, 'weight':'bold'}, title=None, shadow=True)

# titles 
axes.set_title('Volcano Plot', fontweight='bold', style='italic', fontsize=30);
axes.set_xlabel(r'$\mathbf{log_2(fold\ change)}$', fontsize=20);
axes.set_ylabel(r"$\mathbf{-log_{10}(p\ value\ corrected)}$", fontsize=20);

# grey lines
plt.axvline(0, linestyle = "--", color='grey', linewidth=3);
plt.axhline(-np.log10(0.05), linestyle = "--", color='grey', linewidth=3);
plt.text(7, -np.log10(0.05)+1,'p value = 0.05', color='grey', fontweight='bold', fontsize=14)

# setting ticks and spines parameters
for spine in axes.spines.values(): spine.set_linewidth(2) 
plt.xticks(range(-10,11,5),weight='bold', fontsize=12)
plt.yticks(weight='bold', fontsize=12)
axes.tick_params(which='major', width=2, length=6)
axes.tick_params(which='minor', width=1.5, length=3)
plt.minorticks_on();

#limits of X axis
plt.xlim([-11, 11]);

# annotating by arrows
for num_of_gene in range(4): 
    axes.annotate(genes_to_annotate.iloc[num_of_gene].Sample, 
                  xy=(genes_to_annotate.iloc[num_of_gene].logFC, 
                      genes_to_annotate.iloc[num_of_gene].log_pval),
                  xytext=(genes_to_annotate.iloc[num_of_gene].logFC + 0.2, 
                          genes_to_annotate.iloc[num_of_gene].log_pval + 13),
                  weight='bold', fontsize=12,
                  arrowprops=dict(linewidth=0.5, facecolor = 'red', 
                                  headlength=8, width=2, headwidth=7, shrink=0.1))


# # Pie chart

# ### Preparing data

# In[35]:


pop_data = pd.read_csv('population_by_country_2020.csv')
pop_data = pop_data.loc[pop_data['Population (2020)']>50000000]
pop_data.head(5)


# In[32]:


# copying data for manipulations
pop_copy = pop_data[['Country (or dependency)','Population (2020)']].copy()
pop_total = pop_copy.loc[:,'Population (2020)'].sum()

# names of countries that will be in "Others" (countries with population <= 130000000)
names_of_others = pop_copy.loc[pop_data['Population (2020)'] <= 130000000, 'Country (or dependency)']
names_of_others = names_of_others.reset_index().iloc[:,1];

# total population of "Others" countries
pop_copy.loc[pop_data['Population (2020)'] <= 130000000, 'Country (or dependency)'] = 'Others'
pop_others = pop_copy.loc[pop_copy['Country (or dependency)'] == 'Others', 'Population (2020)'].sum()

# making data with populations of countries + Others for pie chart
row_of_others = pd.DataFrame(data={'Country (or dependency)':['Others'], 'Population (2020)':[pop_others]})
data_for_pie = pd.concat([pop_copy.loc[pop_data['Population (2020)'] >= 130000000], row_of_others]).reset_index().iloc[:,[1,2]]

# names of countries + Others
names_of_countries = data_for_pie['Country (or dependency)']

data_for_pie


# ### Pie chart!

# In[27]:


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 8))

ax1.set_zorder(1)
ax2.set_zorder(0)

# PIE
plt.suptitle('Populations of countries with population greater then 5 million', weight='bold', fontsize=18)
fig.subplots_adjust(wspace=0)
angle = 85

wedges, text = ax1.pie(data_for_pie['Population (2020)'],
                    explode = tuple([0]*9+[0.05]), startangle=angle);

theta1, theta2 = wedges[9].theta1, wedges[9].theta2
center, r = wedges[9].center, wedges[9].r

for i, p in enumerate(wedges):
    ang = (p.theta2 - p.theta1)/2 + p.theta1
    y = np.sin(np.deg2rad(ang))
    x = np.cos(np.deg2rad(ang))
    ax1.annotate(f"{names_of_countries[i]} ({data_for_pie.iloc[i,1]/pop_total:.2%})", xy=(x, y), 
                 xytext=(1.2*np.sign(x), 1.2*y), weight='bold', fontsize = 9,
                 arrowprops=dict(linewidth=1, arrowstyle="-", connectionstyle="angle, angleA=0, angleB=90"), 
                 bbox=dict(boxstyle="round", fc="w" , lw=0.7, alpha=1, clip_on=True))

# BARPLOT
ax2.axis('off')
ax2.set_xlim(-1.5 * width, 1.5 * width)
bottom = 0
width = 2

for j, (height, label) in enumerate([*zip(pop_data.loc[pop_data['Population (2020)'] <= 130000000, 
                                                       'Population (2020)'], names_of_others)]):
    bottom -= height
    bc = ax2.bar(0, height, width, bottom=bottom, label=label, alpha=0.9)
    ax2.bar_label(bc, labels=[f"{names_of_others[j]} ({height/pop_total:.2%}) "], 
                  label_type='center', fontsize=8, weight='bold')

    
#Connection lines
x = r * np.cos(np.pi / 180 * theta2) + center[0]
y = r * np.sin(np.pi / 180 * theta2) + center[1]
con = ConnectionPatch(xyA=(-width / 2, 0), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
con.set_linewidth(2)
ax2.add_artist(con)

x = r * np.cos(np.pi / 180 * theta1) + center[0]
y = r * np.sin(np.pi / 180 * theta1) + center[1]
con = ConnectionPatch(xyA=(-width / 2, -pop_others), coordsA=ax2.transData,
                      xyB=(x, y), coordsB=ax1.transData)
ax2.add_artist(con)
con.set_linewidth(2)


# ## EDA

# In[23]:


covid_df = pd.read_csv('owid-covid-data.csv')
covid_df


# ## Total number of cases of infection on the continents

# In[24]:


continent_data = covid_df.loc[covid_df.date =='9/30/2022'].groupby('continent').total_cases.sum().reset_index()


# In[156]:


fig, _ = plt.subplots(figsize=(3,3))
plt.pie(x=continent_data.total_cases, labels=continent_data.continent, rotatelabels=False);


# **I assume that Africa simply lacks data, as it is a large continent where epidemics often occur. Africa has weak medicine and badly tracks statistics of disease. It is possible to find out the lack of data by looking through the number of cases per inhabitant of the continent: for other continents where medicine is well developed and statistics are well monitored this number will be +- the same (or at least the order)**

# In[121]:


continent_data['total_cases divided on population'] = \
continent_data.total_cases/(pd.Series([1427, 4723, 744, 607 ,45, 442])*(10**6))
continent_data


# **Information about continents population was obtained from internet. Number of cases per inhabitant of the continent in Africa is 1-2 orders of magnitude less than in other continents. Therefore, we can assume the lack of data recived from Africa**
# 
# Also some problem with data have Asia. It could be connected with China

# In[149]:


countries = covid_df.loc[covid_df.date =='9/30/2022'].groupby('location').total_cases.sum().reset_index()
cases_china = countries.loc[countries.location == "China"].reset_index()
pop_of_china = 1.412*(10**9)
cases_china['cases divided on population'] = cases_china.total_cases/pop_of_china
cases_china


# China is the most populated country not only in Asia, but in the world. And such small number of cases is obviously affect this statistic

# ### First reports about cases

# In[117]:


non_zero_cases = covid_df.loc[(pd.notnull(covid_df.total_cases))&
                              (pd.notnull(covid_df.continent))].copy()

dates = pd.to_datetime(non_zero_cases.groupby("location").
                       date.head(1)).sort_values().head(20)


# In[110]:


covid_df.loc[pd.to_datetime(covid_df.date.sort_index()).index .isin(dates.index)].sort_values(by='date')


#  **It can be assumed that in China the spread of the disease started long before the first reported number of cases in this country. This can be confirmed by comparing the dynamics of new cases in other countries.**
