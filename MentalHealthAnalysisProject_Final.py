#!/usr/bin/env python
# coding: utf-8

# In[37]:


import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio


st.set_page_config(layout="wide")

mypath = "/Users/idinal/Desktop/Data_Science/"

mh = pd.read_csv(mypath+'MentalHealth.csv',index_col = 0,nrows=6468)
mh.index.name = None

mh_type = type(mh)
mh_shape = mh.shape


mh['sum'] = mh['Schizophrenia (%)'] + mh['Bipolar disorder (%)'] + mh['Eating disorders (%)'] + mh['Anxiety disorders (%)'] + mh['Drug use disorders (%)'] + mh['Depression (%)'] + mh['Alcohol use disorders (%)']


new_columns = []
for i in mh.columns:
    if 'disorder' in i.split(' ') or 'disorders' in i.split(' ') or '(%)' in i.split(' '):
        i = i.split(' ')[0]
    new_col = i.lower()
    new_columns.append(new_col)
mh.columns = new_columns


mh['schizophrenia'] = mh['schizophrenia'].astype(float)
mh['bipolar'] = mh['bipolar'].astype(float)
mh['eating'] = mh['eating'].astype(float)


schizophrenia = mh["schizophrenia"]
bipolar = mh["bipolar"]
eating = mh["eating"]
anxiety = mh["anxiety"]
drug = mh["drug"]
depression = mh["depression"]
alcohol = mh["alcohol"]
countries = mh["entity"]
years = mh["year"]


def create_cat(col):
    col_33 = 0.62101746
    col_66 = 2.868053
    new_name = col + "_category"
    mh[new_name] = None
    mh.loc[mh[col]>col_66,new_name] = 'High'
    mh.loc[(mh[col]>col_33) & (mh[col]<col_66),new_name] = 'Medium'
    mh.loc[mh[col]<col_33,new_name] = 'Low'
    
for i in ["schizophrenia","bipolar","eating","anxiety","drug","depression","alcohol","sum"]:
    create_cat(i)

world_happiness_2021 = pd.read_csv(mypath+'world-happiness-report-2021.csv')
country_region = world_happiness_2021[['Country name','Regional indicator']].set_index('Country name')
cr_dict = country_region.to_dict()['Regional indicator']
exceptions_cr_dict = {"Cote d'Ivoire":"Sub-Saharan Africa",
                      "American Samoa":"North America and ANZ",
                      "Andorra":"Western Europe",
                      "Angola":"South Africa",
                      "Antigua and Barbuda":"Latin America and Caribbean",
                      "Australasia":"North America and ANZ",
                      "Bahamas":"North America and ANZ",
                      "Barbados":"North America and ANZ",
                      "Belize":"North America and ANZ",
                      "Bermuda":"North America and ANZ",
                      "Bhutan":"South Asia",
                      "Brunei":"Southeast Asia",
                      "Cape Verde":"South Africa",
                      "Congo":"South Africa",
                      "Cote d'Ivoire":"Middle East and North Africa",
                      "Cuba":"North America and ANZ",
                      "Democratic Republic of Congo":"South Africa",
                      "Djibouti":"Middle East and North Africa",
                      "Dominica":"North America and ANZ",
                      "England":"Western Europe",
                      "Equatorial Guinea":"South Africa",
                      "Eritrea":"Middle East and North Africa",
                      "Fiji":"North America and ANZ",
                      "Greenland":"North America and ANZ",
                      "Grenada":"North America and ANZ",
                      "Guam":"North America and ANZ",
                      "Guinea-Bissau":"Middle East and North Africa",
                      "Guyana":"Latin America and Caribbean",
                      "Kiribati":"North America and ANZ",
                      "Macedonia":"Central and Eastern Europe",
                      "Marshall Islands":"North America and ANZ",
                      "Micronesia (country)":"North America and ANZ",
                      "North Korea":"East Asia",
                      "Northern Ireland":"Western Europe",
                      "Northern Mariana Islands":"North America and ANZ",
                      "Oceania":"North America and ANZ",
                      "Oman":"West Asia",
                      "Palestine":"Middle East and North Africa",
                      "Papua New Guinea":"North America and ANZ",
                      "Puerto Rico":"North America and ANZ",
                      "Qatar":"West Asia",
                      "Saint Lucia":"North America and ANZ",
                      "Saint Vincent and the Grenadines":"Latin America and Caribbean",
                      "Samoa":"North America and ANZ",
                      "Sao Tome and Principe":"South Africa",
                      "Scotland":"Western Europe",
                      "Seychelles":"South Africa",
                      "Solomon Islands":"North America and ANZ",
                      "Somalia":"South Africa",
                      "South Sudan":"Middle East and North Africa",
                      "Sudan":"Middle East and North Africa",
                      "Suriname":"Latin America and Caribbean",
                      "Syria":"Middle East and North Africa",
                      "Taiwan":"East Asia",
                      "Timor":"Southeast Asia",
                      "Tonga":"North America and ANZ",
                      "Trinidad and Tobago":"North America and ANZ",
                      "Tropical Latin America":"Latin America and Caribbean",
                      "United States Virgin Islands":"North America and ANZ",
                      "Vanuatu":"North America and ANZ",
                      "Wales":"Western Europe"}
merged_cr_dict = {**cr_dict, **exceptions_cr_dict}
mh['region'] = mh['entity'].map(merged_cr_dict)
non_country = mh[mh['region'].isnull()]['entity'].unique()
non_country_mh = mh[mh['entity'].isin(non_country)]
country_mh = mh.drop(non_country_mh.index)
china = country_mh.groupby('entity').get_group('China')
usa = country_mh.groupby('entity').get_group('United States')
japan = country_mh.groupby('entity').get_group('Japan')
cuj = pd.concat([china,usa,japan])
health_life = world_happiness_2021['Healthy life expectancy']
rainbow = ['#ff3399','#ff0066','#ff6666','#ff9966','#ffcc66',
            '#ffff66','#ccff33','#99ff33','#66ff33','#33cc33',
            '#00cc00','#00cc66','#00cc99','#009999','#33cccc',
            '#99ff99','#0099cc','#00ccff','#0099ff','#0000ff',
            '#6699ff','#6666ff','#9999ff','#9966ff','#cc99ff',
            '#ff00ff','#ccccff','#cc0099','#ff66cc','#ffcccc']
comments = pd.read_csv(mypath+'mental_health_comments.csv')
wpop = pd.read_csv(mypath+'world_population.csv')


wh = pd.read_csv(mypath+'world-happiness-report.csv')
world_happiness_2021['year'] = 2021
def clean_wh_col(df):
    new_Columns = []
    for c in df.columns:
        if c == 'Country name':
            new_c = 'entity'
        elif c == 'Regional indicator':
            new_c = 'region'
        elif c == 'Healthy life expectancy':
            new_c = 'health'
        elif c == 'Freedom to make life choices':
            new_c = 'freedom'
        elif c == 'Logged GDP per capita':
            new_c = 'economy'
        elif c == 'Dystopia + residual':
            new_c = 'dystopia_residual'
        elif c == 'Ladder score':
            new_c = 'happiness_score'
        else:
            new_c = '_'.join(c.split(' ')).lower()
        new_Columns.append(new_c)
    return new_Columns
world_happiness_2021.columns = clean_wh_col(world_happiness_2021)
world_happiness_2021.drop(columns=['explained_by:_log_gdp_per_capita', 'explained_by:_social_support',
       'explained_by:_healthy_life_expectancy',
       'explained_by:_freedom_to_make_life_choices',
       'explained_by:_generosity', 'explained_by:_perceptions_of_corruption','standard_error_of_ladder_score','upperwhisker','lowerwhisker','region', 'ladder_score_in_dystopia','dystopia_residual'],axis=1,inplace=True)


wh.columns = ['entity', 'year', 'happiness_score', 'economy',
       'social_support', 'health',
       'freedom', 'generosity',
       'perceptions_of_corruption', 'positive', 'negative']
wh.drop(columns=['positive','negative'],axis=1,inplace=True)


merged_wh = pd.concat([wh,world_happiness_2021])
groupby_entity = merged_wh.groupby('entity')
#This cell is for reindexing the dataframe to make sure one country's data stays together
group_list = []
for c in merged_wh['entity'].unique():
    group = groupby_entity.get_group(c)
    group_list.append(group)
new_wh = pd.concat(group_list,axis=0).reset_index(drop=True)


region_grouped = country_mh.groupby('region')


means = region_grouped['sum'].mean().sort_values(ascending=False)


merged_mh = pd.merge(country_mh,new_wh,how='left',on=['entity','year'])
merged_mh.drop(columns='code',inplace=True,axis=1)


columns_to_drop=['CCA3','Continent','Rank','1980 Population','1970 Population','Growth Rate','Capital','Area (km²)','Density (per km²)','World Population Percentage']
merged_pop = pd.concat([wpop.drop(columns_to_drop,axis=1),pd.DataFrame({str(year):[np.nan]*wpop.shape[0] for year in range(1990,2022) if year not in [1990,2000,2010,2015,2020]})],axis=1)
merged_pop = merged_pop.rename(mapper={'Country/Territory':'entity'},axis=1)


melted_pop = pd.melt(merged_pop,id_vars = ['entity'],var_name='year',value_name='population')
melted_pop['year'] = melted_pop['year'].str.extract(r'(\d+)').astype(int)
melted_pop.sort_values(['entity','year'],inplace=True,ignore_index=True)
melted_pop['population'] = melted_pop['population'].ffill()


wp_mh = merged_mh.merge(melted_pop,how='left',on=['entity','year'])
wp_mh["health"] /= 10

color_scales = ["Plotly3","Viridis","Cividis","Inferno","Magma","Plasma","Turbo","Blackbody","Bluered","Electric","Hot","Jet","Rainbow","Blues","BuGn","BuPu","GnBu","Greens","Greys","OrRd","Oranges","PuBu","PuBuGn","PuRd","Purples","RdBu","RdPu","Reds","YlGn","YlGnBu","YlOrBr","YlOrRd","turbid","thermal","haline","solar","ice","gray","deep","dense","algae","matter","speed","amp","tempo","Burg","BurgYl","Redor","Oryel","Peach","Pinkyl","Mint","Blugrn","Darkmint","Emrld","Aggrnyl","Bluyl","Teal","Tealgrn","Purp","Purpor","Sunset","Magenta","Sunsetdark","Agsunset","Brwnyl"]

mental_dict = {"schizophrenia" : "Schizophrenia (%)",
            "anxiety" : "Anxiety (%)",
            "bipolar" : "Bipolar Disorder (%)",
            "eating" : "Eating Disorder(%)",
            "drug" : "Drug Use Disorder(%)",
            "depression" : "Depression(%)",
            "alcohol" : "Alchohol Use Disorders (%)",
            "sum" : "Sum of all the disorders above (%)"}

happiness_dict = {"happiness_score" : "Happiness Score",
                  "economy" : "Economy Index",
                  "social_support" : "Social Support Index",
                  "health" : "Health Index",
                  "freedom" : "Freedom Index",
                  "generosity" : "Generosity Index",
                  "perceptions_of_corruption" : "Perception of Corruption",
                  "population" : "Population"}


cat_dict = {"entity" : "Country",
            "region" : "Region",
            "anxiety_category" : "Anxiety Category",
            "schizophrenia_category":"Schizophrenia Category",
            'bipolar_category':"Bipolar Disorder Category",
            'eating_category':"Eating Disorder Category", 
            'drug_category':"Drug Use Disorder Category", 
            'depression_category':"Depression Category",
            'alcohol_category':"Alcohol Use Disorder Category", 
            'sum_category':"Sum of all the mental problems category"}


all_dict = mental_dict.copy()
all_dict.update(happiness_dict)
all_dict.update(cat_dict)








with st.sidebar: 
	selected = option_menu(
		menu_title = 'Navigation Pane',
		options = ['Abstract', 'Background Information', 'Data Cleaning', "Exploratory Analysis",  'General analysis','Focus analysis on different continents','Focus analysis on Canada, China, the US and UK', 'Conclusion', 'Bibliography'],
		menu_icon = 'stars',
		icons = ['door-open', 'easel3-fill', 'emoji-dizzy-fill', 'dpad-fill', 'emoji-frown', 'emoji-neutral', 'emoji-grin', 'egg-fried', 'door-closed-fill'],
		default_index = 0
		)


if selected=='Abstract':
    st.title("Mental Health")
    st.markdown("Have you ever experienced anxiety or stress? In a world where mental health problems often overshadow our lives, understanding the  interconnection between mental health and happiness could be the key to unlocking a more fulfilling existence. What if nurturing our minds could lead us to a brighter, more joyful future?")
    st.markdown("Based on two given datasets, we are going to explore how different types of mental health issues affect the happiness indeces of each country. To answer your questions, let’s dive into the analysis!")
    




    
if selected=="Background Information":
    st.title("Background Information")
    st.markdown("The relationship between mental health and happiness has gatherd significant attention in recent years, as researchers seek to find the scientific factors that contribute to overall well-being. Mental health is defined by the World Health Organization (WHO) as a state of well-being in which individuals realize their potential, can cope with the normal stresses of life, and can contribute to their community (WHO). This definition highlights how mental health can affect one in emotional, psychological, and social ways. ")
    st.markdown("Studies have shown that mental health directly influences happiness. For instance, a meta-analysis by Wood et al. (2010) <sup>5</sup> found a strong correlation between positive mental health and life satisfaction, suggesting that individuals who engage in practices that promote mental well-being, such as mindfulness and social connections, tend to report higher levels of happiness. Furthermore, research by Keyes (2002)<sup>2</sup> emphasizes the importance of flourishing—defined as a high level of mental health—indicating that those who flourish experience greater happiness and life satisfaction compared to those who merely survive.", unsafe_allow_html=True)
    st.markdown("The data used in this analysis includes survey responses from a diverse population that measures various aspects of mental health (e.g., depression, anxiety, and bipolar disorders). This dataset allows us to manipulate data in order to find the relationship between mental health and happiness, supporting the thesis that enhancing mental health can significantly improve overall happiness. By employing statistical methods such as regression analysis, we can identify specific mental health factors that predict happiness, providing valuable insights for interventions.")






if selected=="Data Cleaning":
    st.title('Data Cleaning')
    st.markdown("The data cleaning process mainly involves converting column names, merging datasets, creating new columns, and mapping datasets with dictionaries.")
    st.markdown("Let's first import the dataset with the first 6468 columns so we have only the data that we will need.")
    st.code('''
            mh = pd.read_csv('MentalHealth.csv',index_col = 0,nrows=6468)
            ''',language='python')
    st.markdown("Then, a new column named 'sum' is created by adding all the mental problem columns together. This column represents the total percentage of mental problem patients in a country. ")
    st.code('''
            mh['sum'] = mh['Schizophrenia (%)'] + mh['Bipolar disorder (%)'] + mh['Eating disorders (%)'] + mh['Anxiety disorders (%)'] + mh['Drug use disorders (%)'] + mh['Depression (%)'] + mh['Alcohol use disorders (%)']
            ''',language='python')
    st.markdown("Next, let's rename the columns into easier versions so they can become convenient to use in future data cleaning. ")
    st.code('''
            new_columns = []
for i in mh.columns:
    if 'disorder' in i.split(' ') or 'disorders' in i.split(' ') or '(%)' in i.split(' '):
        i = i.split(' ')[0]
    new_col = i.lower()
    new_columns.append(new_col)
mh.columns = new_columns
            ''',language='python')
    st.markdown("For graph making, let's create new category columns by creating a function that can help us do all that in one for loop. In the process, we will need to calculate the overall quantiles of this dataset. ")
    st.code('''
            def create_cat(col):
    col_33 = 0.62101746
    col_66 = 2.868053
    new_name = col + "_category"
    mh[new_name] = None
    mh.loc[mh[col]>2.868053,new_name] = 'High'
    mh.loc[(mh[col]>0.62101746) & (mh[col]<2.868053),new_name] = 'Medium'
    mh.loc[mh[col]<0.62101746,new_name] = 'Low'
    for i in ["schizophrenia","bipolar","eating","anxiety","drug","depression","alcohol","sum"]:
    create_cat(i)
            ''',language='python')
    st.markdown("Now, let's import a new dataset that include the happiness index of 2021 from all over the world. This way, we can analyze the relationship between happiness index and mental health percentages. ")
    st.code('''
            world_happiness_2021 = pd.read_csv('world-happiness-report-2021.csv')
            ''',language='python')
    st.markdown("After importingh this dataset, we will need to merge it with the previous dataset that we have. To do this, we will need to map the countries in this happiness index dataset into the mental health dataset that we have. ")
    st.code('''
            country_region = world_happiness_2021[['Country name','Regional indicator']].set_index('Country name')
cr_dict = country_region.to_dict()['Regional indicator']
            ''',language='python')
    st. markdown("Here,we can create a dictionary that can be used to map the two dictionary together. This dictionary is created by research and it includes all the countries that are not included in the previous dictionary 'cr_dict'. This way, all the countries will be included and  then we can classify the countries into different regions. ")
    with st.expander("See the exceptioal cr dict"):
        st.code('''
        exceptions_cr_dict = {"Cote d'Ivoire":"Sub-Saharan Africa",
                      "American Samoa":"North America and ANZ",
                      "Andorra":"Western Europe",
                      "Angola":"South Africa",
                      "Antigua and Barbuda":"Latin America and Caribbean",
                      "Australasia":"North America and ANZ",
                      "Bahamas":"North America and ANZ",
                      "Barbados":"North America and ANZ",
                      "Belize":"North America and ANZ",
                      "Bermuda":"North America and ANZ",
                      "Bhutan":"South Asia",
                      "Brunei":"Southeast Asia",
                      "Cape Verde":"South Africa",
                      "Congo":"South Africa",
                      "Cote d'Ivoire":"Middle East and North Africa",
                      "Cuba":"North America and ANZ",
                      "Democratic Republic of Congo":"South Africa",
                      "Djibouti":"Middle East and North Africa",
                      "Dominica":"North America and ANZ",
                      "England":"Western Europe",
                      "Equatorial Guinea":"South Africa",
                      "Eritrea":"Middle East and North Africa",
                      "Fiji":"North America and ANZ",
                      "Greenland":"North America and ANZ",
                      "Grenada":"North America and ANZ",
                      "Guam":"North America and ANZ",
                      "Guinea-Bissau":"Middle East and North Africa",
                      "Guyana":"Latin America and Caribbean",
                      "Kiribati":"North America and ANZ",
                      "Macedonia":"Central and Eastern Europe",
                      "Marshall Islands":"North America and ANZ",
                      "Micronesia (country)":"North America and ANZ",
                      "North Korea":"East Asia",
                      "Northern Ireland":"Western Europe",
                      "Northern Mariana Islands":"North America and ANZ",
                      "Oceania":"North America and ANZ",
                      "Oman":"West Asia",
                      "Palestine":"Middle East and North Africa",
                      "Papua New Guinea":"North America and ANZ",
                      "Puerto Rico":"North America and ANZ",
                      "Qatar":"West Asia",
                      "Saint Lucia":"North America and ANZ",
                      "Saint Vincent and the Grenadines":"Latin America and Caribbean",
                      "Samoa":"North America and ANZ",
                      "Sao Tome and Principe":"South Africa",
                      "Scotland":"Western Europe",
                      "Seychelles":"South Africa",
                      "Solomon Islands":"North America and ANZ",
                      "Somalia":"South Africa",
                      "South Sudan":"Middle East and North Africa",
                      "Sudan":"Middle East and North Africa",
                      "Suriname":"Latin America and Caribbean",
                      "Syria":"Middle East and North Africa",
                      "Taiwan":"East Asia",
                      "Timor":"Southeast Asia",
                      "Tonga":"North America and ANZ",
                      "Trinidad and Tobago":"North America and ANZ",
                      "Tropical Latin America":"Latin America and Caribbean",
                      "United States Virgin Islands":"North America and ANZ",
                      "Vanuatu":"North America and ANZ",
                      "Wales":"Western Europe"}
        ''',language='python')
    st.markdown("After creating this exceptional dictionary, we can merge it with the previous dictionary and use it for mapping the two datasets, ")
    st.code('''
            merged_cr_dict = {**cr_dict, **exceptions_cr_dict}
mh['region'] = mh['entity'].map(merged_cr_dict)
            ''')
    st.markdown("After mapping these two datasets, let's add a new dataset which includes the comments from different mental problem patients on twitter. ")
    st.code('''
            comments = pd.read_csv('mental_health_comments.csv')

            ''',language='python')
    st.markdown("Next, let's include another dataset which inludes the happiness index data from 2005-2020, this dataset can help fill in the gap from the previous happiness index dataset which only included the data from 2021. ")
    st.code('''
            wh = pd.read_csv('world-happiness-report.csv')
            ''',language='python')
    st.markdown("Also, I added another dataset which includes world population data that will hopefullt help with our investigation and analysis. ")
    st.code('''
            wpop = pd.read_csv('world_population.csv')
            ''',language='python')
    st.markdown("This is a function for cleaning the column names for the newly added datasets to make sure that the columns with the same meanings have the same name. For example, 'Country name' and 'entity' are the same columns but are named differently in two datasets. So, we will need to unify them using this function. the first few if and elif statements are taking care of the exceptions which can not simply be transformed into the cleaned form. And the final else statement is for cleaning the other statements that have not existed in other datasets. ")
    st.code('''
            def clean_wh_col(df):
    new_Columns = []
    for c in df.columns:
        if c == 'Country name':
            new_c = 'entity'
        elif c == 'Regional indicator':
            new_c = 'region'
        elif c == 'Healthy life expectancy':
            new_c = 'health'
        elif c == 'Freedom to make life choices':
            new_c = 'freedom'
        elif c == 'Logged GDP per capita':
            new_c = 'economy'
        elif c == 'Dystopia + residual':
            new_c = 'dystopia_residual'
        elif c == 'Ladder score':
            new_c = 'happiness_score'
        else:
            new_c = '_'.join(c.split(' ')).lower()
        new_Columns.append(new_c)
    return new_Columns
            ''',language='python')
    with st.expander("This cell is for reindexing the dataframe to make sure one country's data stays together"):
        st.code('''
                merged_wh = pd.concat([wh,world_happiness_2021])
groupby_entity = merged_wh.groupby('entity')
group_list = []
for c in merged_wh['entity'].unique():
    group = groupby_entity.get_group(c)
    group_list.append(group)
new_wh = pd.concat(group_list,axis=0).reset_index(drop=True)
                ''',language='python')
    st.markdown("Lastly, we can merge all the datasets we have cleaned together using the pd.merge() function. By clarifying the how parameter, we can choose which column in the datasets they have in common and use them as indicators for the merge. ")
    st.code('''
            merged_mh = pd.merge(country_mh,new_wh,how='left',on=['entity','year'])
merged_mh.drop(columns='code',inplace=True,axis=1)
            ''',language='python')
    
    st.markdown("Now, we will take a look at the cleaned dataset that's ready for analysis:")
    st.code('''
            print(wp_mh)
            ''',language='python')
    st.dataframe(wp_mh)

if selected=="Exploratory Analysis":

    st.title('Exploratory Analysis')
    
    st.markdown("### Scatter: Two Numeric")
    st.markdown("For this scatter plot, select one mental problem variable and one happiness index to check the relationship between these two variables.")
    st.markdown("To understand this graph, you should expect to see a general trend through the scatters. The trend will be indicating the relationship betweent the mental problem and happiness index you chose. A trend with positive slope would mean the higher the percentage of the mental disease means higher the happiness index and vice versa. ")
    col_37,col_38 = st.columns([2,5])
    
    
    with st.form("Scatter: Two Numeric"):
        col_37_x = col_37.selectbox("Choose an numeric variable for the x-axis", mental_dict.values(),key=1)
        col_37_xdf = [k for k,v in mental_dict.items() if v == col_37_x][0]
        
        
        col_37_y = col_37.selectbox("Choose an numeric variable for the y-axis",happiness_dict.values(),key=2)
        col_37_ydf = [k for k,v in happiness_dict.items() if v == col_37_y][0]
        
                    
        submitted=st.form_submit_button("Submit to produce the histogram")
        if submitted:
            fig1 = px.scatter(wp_mh,x=col_37_xdf,y=col_37_ydf,labels=all_dict,title=f"<b>Average of {col_37_y} by {col_37_x}<\b>")
            col_38.plotly_chart(fig1)
            
            
            
            
            
            
            
            
            
    st.subheader("Pie: Distribution of category")
    
    col_91,col_92 = st.columns([2,5])
    
    with st.form("Pie: Distribution of category"):   
        
        col_91_x = col_91.selectbox("Choose an mental problem for the pie chart", np.setdiff1d(list(cat_dict.values()),["Country","Region","Sum of all the mental problems category"]),key=1000)
        col_91_xdf = [k for k,v in cat_dict.items() if v == col_91_x][0]
        
        
        submitted=st.form_submit_button("Submit to produce the pie chart")
        if submitted:
            fig16 = px.pie(wp_mh,names=col_91_xdf)
            fig16.update_traces(textposition='inside', textinfo='percent+label')
            fig16.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
            col_92.plotly_chart(fig16)
        
        
        
        
        
        
        
        
        
        
       
    st.subheader("Histogram: Categorized Mental Problem in Regions")
    st.markdown("For this histogram, choose a mental problem category to check the situation of that mental problem in regions")
    st.markdown("This graph shows how a mental problem percentage data is spread in a region.")
    col_39,col_40 = st.columns([2,5])
    
    
    with st.form("Histogram: Categorized Mental Problem in Regions"):
        
        col_39_color = col_39.selectbox("Choose an category variable for the y-axis", np.setdiff1d(list(cat_dict.values()),["Country","Region"]),key=6)
        col_39_colordf = [k for k,v in cat_dict.items() if v == col_39_color][0]
        
        col_39_checkbox = col_39.checkbox("Choose to specify the number of bins",key=7) #boolean
        bins = 10
        if col_39_checkbox:
            col_39_number_input = col_39.number_input("Enter a number to specify the number of bins", min_value=5, placeholder="Type a number...",key=16)
            bins = col_39_number_input
            
        col_39_norm = col_39.radio("Choose a function for the y-axis",["Total","Histnorm Percent","Barnorm Percent"],key=31)
        if col_39_norm == "Total":
            col_39_normdh = ""
            col_39_normdb = ""
        elif col_39_norm == "Histnorm Percent":
            col_39_normdh = "percent"
            col_39_normdb = ""
        else:
            col_39_normdh = ""
            col_39_normdb = "percent"
            
            
        submitted=st.form_submit_button("Submit to produce the histogram")
        if submitted:
            fig2 = px.histogram(wp_mh,x="region",color=col_39_colordf, nbins=bins,labels=all_dict,histfunc="avg",barmode="group",title=f"<b>Average of {col_39_color} by Region<\b>",histnorm=col_39_normdh,barnorm=col_39_normdb)
            col_40.plotly_chart(fig2)
            
            
            
            
            
            
            
            
    st.subheader("Boxplot: Happiness Index in Countries or Regions")
    st.markdown("Choose one happiness index for the x-axis and one category variable for the color to check the spread of happiness index in regions or countries")
    st.markdown("This boxplot shows the spread of happiness index you chose in regions or the countries chosen. ")
    col_41,col_42 = st.columns([2,5])
    
    
    with st.form("Boxplot: Happiness Index in Countries or Regions"):
        
        col_41_radio = col_41.radio("Choose a x-axis variable type for the boxplot graph",["Country","Region"])
        
        if col_41_radio == "Country":
            col_41_choice = col_41.multiselect("Choose Country", wp_mh[wp_mh["happiness_score"].notnull()]["entity"].unique())
            col_41_x = "entity"
        else:
            col_41_choice = wp_mh[wp_mh["happiness_score"].notnull()]["entity"].unique()
            col_41_x = "region"
        
        col_41_y = col_41.selectbox("Choose an numeric variable for the y-axis", happiness_dict.values(),key=9)
        col_41_ydf = [k for k,v in happiness_dict.items() if v == col_41_y][0]
        
        col_41_color = col_41.selectbox("Choose an category variable for the color of the histogram",np.setdiff1d(list(cat_dict.values()),"Country"),index=6,key=11)
        col_41_colordf = [k for k,v in cat_dict.items() if v == col_41_color][0]
        
        col_41_point = col_41.radio("Do you wish to display all points on the boxplot?",["Yes","No"])
        if col_41_point == 'Yes':
            col_41_pointdf = "all"
        else:
            col_41_pointdf = None
        
            
        submitted=st.form_submit_button("Submit to produce the boxplot")
        if submitted:
            col_41_df = wp_mh[wp_mh['entity'].isin(col_41_choice)]
            fig3 = px.box(col_41_df,x=col_41_x,y=col_41_ydf,color=col_41_colordf, labels=all_dict,color_discrete_sequence=rainbow,title=f"<b>Average of {col_41_y} by country and {col_41_color}<\b>",points=col_41_pointdf)
            col_42.plotly_chart(fig3)
            st.markdown("This boxplot shows the range of happiness scores of countries and one type of mental problem category")
            
            

            
    
    st.subheader("Scatter: Country mental health over years")
    st.markdown("Choose the countries you want to investigate and choose a mental problem to check the trend of mental problem over the years in theses countries.")
    st.markdown("This scatter plot will show a trend of a certain mental health problem in the countries you chose. ")
    col_43,col_44 = st.columns([2,5])
    
    with st.form("Scatter: Country mental health over years"):
        col_43_choice = col_43.multiselect("Choose Country", wp_mh['entity'].unique(),key=15)
        

        
        col_43_y = col_43.selectbox("Choose an mental problem for the y-axis", mental_dict.values(),key=12)
        col_43_ydf = [k for k,v in mental_dict.items() if v == col_43_y][0]
        
            
            
        submitted=st.form_submit_button("Submit to produce the histogram")
        if submitted:
            col_43_df = wp_mh[wp_mh['entity'].isin(col_43_choice)]
            fig4 = px.scatter(col_43_df,x="year",y=col_43_ydf,color="entity", labels=all_dict,title=f"<b>Average of {col_43_y} by Year<\b>")
            fig4.update_xaxes(type="category")
            col_44.plotly_chart(fig4)
        st.markdown("This graph shows the trend of one mental problem in countries")
            
            
            
            
    st.subheader("Line: Country happiness indeces over years")
    st.markdown("Choose the countries you want to investigate and choose a happiness index to check the trend of mental problem over the years in theses countries.")
    col_45,col_46 = st.columns([2,5])
    
     
    with st.form("Line: Country happiness indeces over years"):
         col_45_choice = col_45.multiselect("Choose Country", wp_mh['entity'].unique(),key=18)
         

         
         col_45_y = col_45.selectbox("Choose a happiness variable for the y-axis", happiness_dict.values(),key=19)
         col_45_ydf = [k for k,v in happiness_dict.items() if v == col_45_y][0]
         
             
         submitted=st.form_submit_button("Submit to produce the line graph")
         if submitted:
             col_45_df = wp_mh[(wp_mh['entity'].isin(col_45_choice))&(wp_mh["year"]>2005)&(wp_mh[col_45_ydf].notnull())]
             fig5 = px.line(col_45_df.sort_values("year"),x="year",y=col_45_ydf,color="entity", labels=all_dict,title=f"<b>Average of {col_45_y} by Year<\b>",markers=True)
             col_46.plotly_chart(fig5)
        
            
        
        
        
    st.subheader("Choropleth Graph: Mental Health Conditions Around the world")
    st.markdown("Choose a mental problem investigate and customize the graph with color scales and displaying methods. ")  
    col_47,col_48 = st.columns([2,5])
     
    with st.form("Choropleth Graph: Mental Health Conditions Around the world"):
            
        col_47,col_48 = st.columns([2,5])
        
        col_47_color = col_47.selectbox("Choose an mental problem for the color",mental_dict.values(),key=16)
        col_47_colordf = [k for k,v in mental_dict.items() if v == col_47_color][0]
        
        col_47_color_scale = col_47.selectbox("Choose an color scale",color_scales,key=17)
        
        col_47_projection = col_47.radio("Choose a projection method for the choropleth graph",["equirectangular","orthographic","mollweide"])
        
        submitted=st.form_submit_button("Submit to produce the choropleth graph")
        
        if submitted:
            fig6 = px.choropleth(wp_mh,locations="entity",locationmode="country names",color=col_47_colordf,color_continuous_scale=col_47_color_scale,projection=col_47_projection)
            col_48.plotly_chart(fig6)
            
    
    
    
    st.subheader("Sunburst Graph: Mental Health Conditions Around the world")
    st.markdown("Choose regions and a mentla problem to investigate the spread of mental problem in the countries in the region selected. ")  
    col_49,col_50 = st.columns([2,5])
     
    with st.form("Sunburst Graph: Mental Health Conditions Around the world"):
            
        col_49,col_50 = st.columns([2,5])
        
        col_49_path = col_49.multiselect("Choose regions you want to investigate!", wp_mh["region"].unique(),key=20)
        
        col_49_value= col_49.selectbox("Choose a mental health problem to investigate!", mental_dict.values(),key=21)
        col_49_valuedf = [k for k,v in mental_dict.items() if v == col_49_value][0]
        
        col_49_color_scale = col_49.selectbox("Choose an color scale",color_scales,key=22)
    
        
        submitted=st.form_submit_button("Submit to produce the sunburst graph")
        
        if submitted:
            col_49_df = wp_mh[(wp_mh['region'].isin(col_49_path))]
            fig7 = px.sunburst(col_49_df,path = ["region","entity"],values=col_49_valuedf,color=col_49_valuedf,color_continuous_scale=col_49_color_scale)
            col_50.plotly_chart(fig7)
            

                
       
    st.subheader("Histogram: Two Category")
    st.markdown("Choose two category variables and a histnorm or barnorm method to check the histogram of the relationship between these two categories!")
    col_51,col_52 = st.columns([2,5])
    
    with st.form("Histogram: Two Category"):
        
        col_51_x = col_51.selectbox("Choose an category variable for the x-axis", np.setdiff1d(list(cat_dict.values()),["Country","Region"]),key=23)
        col_51_xdf = [k for k,v in cat_dict.items() if v == col_51_x][0]
        
        col_51_color = col_51.selectbox("Choose an category variable for the color", np.setdiff1d(list(cat_dict.values()),[col_51_x,"Country"]),key=25)
        col_51_colordf = [k for k,v in cat_dict.items() if v == col_51_color][0]
        
        col_51_norm = col_51.radio("Choose a function for the y-axis",["Total","Histnorm Percent","Barnorm Percent"],key=27)
        if col_51_norm == "Total":
            col_51_normdh = ""
            col_51_normdb = ""
        elif col_51_norm == "Histnorm Percent":
            col_51_normdh = "percent"
            col_51_normdb = ""
        else:
            col_51_normdh = ""
            col_51_normdb = "percent"
        
        col_51_checkbox = col_51.checkbox("Choose to specify the number of bins",key=24) #boolean
        bins = 10
        if col_51_checkbox:
            col_51_number_input = col_51.number_input("Enter a number to specify the number of bins", min_value=5, placeholder="Type a number...",key=26)
            bins = col_51_number_input
            
            
        submitted=st.form_submit_button("Submit to produce the histogram")
        if submitted:
            fig8 = px.histogram(wp_mh,x=col_51_xdf,color=col_51_colordf, nbins=bins,labels=all_dict,histfunc="avg",barmode="group",title=f"<b>Average of {col_51_x} by {col_51_color}<\b>",histnorm=col_51_normdh,barnorm=col_51_normdb)
            col_52.plotly_chart(fig8)
            
            
            
            
          
    st.subheader("Histogram: Mental Problems in Countries")
    st.markdown("Choose countries and mental problems to check the histogram and choose the histnorm and barnorm method to customize your histogram. ")
    col_53,col_54 = st.columns([2,5])
    
    
    with st.form("Histogram: Mental Problems in Countries"):
        col_53_x = col_53.multiselect("Choose Country", wp_mh["entity"].unique(),key=29)
        
        col_53_y = col_53.multiselect("Choose mental problems for the y-axis", mental_dict.values(),key=28)
        col_53_ydf = [k for k,v in mental_dict.items() if v in col_53_y]
        
        col_53_norm = col_53.radio("Choose a function for the y-axis",["Total","Histnorm Percent","Barnorm Percent"],key=30)
        if col_53_norm == "Total":
            col_53_normdh = ""
            col_53_normdb = ""
        elif col_53_norm == "Histnorm Percent":
            col_53_normdh = "percent"
            col_53_normdb = ""
        else:
            col_53_normdh = ""
            col_53_normdb = "percent"
        
            
        submitted=st.form_submit_button("Submit to produce the histogram")
        if submitted:
            col_53_df = wp_mh[wp_mh['entity'].isin(col_53_x)]
            fig9 = px.histogram(col_53_df,x="entity",y=col_53_ydf, labels=all_dict,color_discrete_sequence=rainbow,histfunc="avg",barmode="group", title=f"<b>Average of {col_53_y} by {col_53_x} </b>",histnorm=col_53_normdh,barnorm=col_53_normdb)
            col_54.plotly_chart(fig9)
            
    
            
            
            
            
            

if selected=="General analysis":
    st.title("General analysis")
    
    
    st.subheader("Overall relationship between mental problem percentages and happiness score")
    col_55,col_56 = st.columns([3,5])
   
    melted_df2 = pd.melt(wp_mh[wp_mh['entity'].isin(["China","United States","United Kingdom","Canada"])],id_vars = ["entity","year"], value_vars =["happiness_score",
                      "economy",
                      "social_support",
                      "health",
                      "freedom",
                      "generosity"],
                         var_name = "happiness_index", value_name = "happiness_value")
    fig = make_subplots(
    rows=4, cols=2,
    subplot_titles=("Schizophrenia", "Depression","Bipolar","Anxiety","Alcohol Disorder","Eating Disorder","Drug Disorder"))
    fig.add_traces(
        go.Scattergl(
            x = wp_mh["schizophrenia"],
            y = wp_mh["happiness_score"],
            mode = "markers",
            marker = {'color': '#ff3399', 'symbol': 'circle'},
            name = "Schizophrenia",
            showlegend = True,
            hovertemplate = 'Schizophrenia (%)=%{x}<br>Happiness Score=%{y}<extra></extra>',
            xaxis = "x",
            yaxis = "y"
            ),rows = 1, cols = 1
        )
    fig.add_traces(
        go.Scattergl(
            x = wp_mh["depression"],
            y = wp_mh["happiness_score"],
            mode = "markers",
            marker = {'color':'#ff0066', 'symbol': 'circle'},
            name = "Depression",
            showlegend = True,
            hovertemplate = 'Depression (%)=%{x}<br>Happiness Score=%{y}<extra></extra>',
            xaxis = "x2",
            yaxis = "y2"
            ),rows = 1, cols = 2
        )
    fig.add_traces(
        go.Scattergl(
            x = wp_mh["bipolar"],
            y = wp_mh["happiness_score"],
            mode = "markers",
            marker = {'color':'#ff6666', 'symbol': 'circle'},
            name = "Bipolar",
            showlegend = True,
            hovertemplate = 'Bipolar (%)=%{x}<br>Happiness Score=%{y}<extra></extra>',
            xaxis = "x3",
            yaxis = "y3"
            ),rows = 2, cols = 1
        )
    fig.add_traces(
        go.Scattergl(
            x = wp_mh["anxiety"],
            y = wp_mh["happiness_score"],
            mode = "markers",
            marker = {'color':'#ff9966', 'symbol': 'circle'},
            name = "Anxiety",
            showlegend = True,
            hovertemplate = 'Anxiety (%)=%{x}<br>Happiness Score=%{y}<extra></extra>',
            xaxis = "x4",
            yaxis = "y4"
            ),rows = 2, cols = 2
        )
    fig.add_traces(
        go.Scattergl(
            x = wp_mh["alcohol"],
            y = wp_mh["happiness_score"],
            mode = "markers",
            marker = {'color':'#ffcc66', 'symbol': 'circle'},
            name = "Alcohol",
            showlegend = True,
            hovertemplate = 'Alcohol (%)=%{x}<br>Happiness Score=%{y}<extra></extra>',
            xaxis = "x5",
            yaxis = "y5"
            ),rows = 3, cols = 1
        )
    fig.add_traces(
        go.Scattergl(
            x = wp_mh["eating"],
            y = wp_mh["happiness_score"],
            mode = "markers",
            marker = {'color':'#ffff66', 'symbol': 'circle'},
            name = "Eating",
            showlegend = True,
            hovertemplate = 'Eating (%)=%{x}<br>Happiness Score=%{y}<extra></extra>',
            xaxis = "x6",
            yaxis = "y6"
            ),rows = 3, cols = 2
        )
    fig.add_traces(
        go.Scattergl(
            x = wp_mh["drug"],
            y = wp_mh["happiness_score"],
            mode = "markers",
            marker = {'color':'#ccff66', 'symbol': 'circle'},
            name = "Drug",
            showlegend = True,
            hovertemplate = 'Drug (%)=%{x}<br>Happiness Score=%{y}<extra></extra>',
            xaxis = "x7",
            yaxis = "y7"
            ),rows = 4, cols = 1
        )
    fig.update_layout(height=1200, width=1000,title_text = "Average of Happiness Score by Mental Problem")
    col_56.plotly_chart(fig)
    
    col_55.markdown("This scatter plot displays the correlations between percentages of people who have a particular type of mental problem and the happiness score responding to this percentage. The x-axis represents the percentage of the chosen mental problem, and the y-axis represents the corresponding happiness score. This graph may look chaotic but we can summarize the trend of each scatter plot present in this graph, including schizophrenia, anxiety disorder, bipolar disorder, eating disorder, drug disorder, depression and alcohol disorder. The plots can be viewed in 2 ways: First, by observing the different density of dots on the graph, we can obtain the distribution of percentage of these different mental problems. Most of the mental problems have the most datapoints when the percentage are low, revealed by the dense block of dots collected on the left side of the x-axis; although these illnesses share the property of denser datapoints around the left end of the x-axis, their data are not the same due to the fact that they do not share the same x-axis scale. For instance, schizophrenia datapoints are collected around 0.16%, while depression datapoints are collected around 3.5%. There is only one exception to this conclusion, bipolar disorder, as shown in the graph, the datapoints of bipolar disorder are gathered around the midpoint of the x-axis, meaning that the distribution of percentages of this illness is dense around 0.75%. Second, the datapoints reveal a trend that demonstrates the correlation between happiness score and mental problems, and increasing trend would indicate that a country who have more patients of this illness will have a higher happiness score, and vice versa. By observing these scatter plots, we can categorize these plots into 2 types, as mentioned before, increasing and decreasing. The scatter plots that shows an increasing trend include: schizophrenia, anxiety disorder, bipolar disorder, eating disorder and drug disorder, this reveals that the higher the percentage of people who have these mental illness, the higher the happiness score of the country. On the other hand, the plots that displays a decreasing trend include: alcohol disorder and depression, meaning that lower the percentage of alcohol disorder and depression patients, higher the happiness score of the country. ")
    
    
    
    
    
    st.subheader("Distribution of category of different mental problems")
    col_75,col_76 = st.columns([2,5])

    df = pd.melt(wp_mh,
                     id_vars = ["entity","year","happiness_score"], 
                     value_vars = ['schizophrenia_category', 
                                   'bipolar_category', 
                                   'eating_category',
                                   'anxiety_category',
                                   'drug_category', 
                                   'depression_category', 
                                   'alcohol_category'], 
                     var_name = "mental_problem_category", 
                     value_name = "category")
    df.groupby(["entity","mental_problem_category","category"])["year"].count().reset_index()
    fig16 = px.pie(df, values='year', names='category',facet_col = "mental_problem_category",facet_col_wrap=3,labels={"year":"num"},facet_row_spacing=0.01,
              facet_col_spacing=0.03,height = 1200, width = 800,title="Distribution of category of different mental problems")
    fig16.update_traces(textposition='inside', textinfo='percent+label')
    fig16.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    col_76.plotly_chart(fig16)
    col_75.markdown("This pie chart displays the distribution of categories of different mental problems. The different colors represent 3 categories, with navy representing low, cerulean representing medium and red representing high. These categories are established by calculating the trisect-points of the entire dataset, this means all of the percentages across various illnesses. By observing this graph, we can see that different illnesses are constructed by different types of datapoints, we are going to identify them one by one. The schizophrenia graph is completely navy, revealing that all of the datapoints of schizophrenia belong to the low category, which means that the percentage of people who have schizophrenia are extremely low. The bipolar disorder graph is 72.7% cerulean and 27.3% navy, meaning that for almost a third of the times, the percentage of bipolar disorder is in the medium range. The eating disorder graph is mostly navy, and has 3.02% cerulean, indicating that most of the datapoints are in the low category. The anxiety disorder graph is mostly red and 8.52% cerulean, meaning that most of the datapoints in anxiety disorder is relatively high. In the drug disorder graph, there is a mix of the three categories; however, the graph is mainly cerulean and containing less than 1% of red. The depression graph is 80.9% red, which means that most of the datapoints in depression belongs to the high category, but it is still less than anxiety disorder. The alcohol disorder graph is mostly cerulean and contains all of the three categories, meaning the datapoints are concentrated in the medium category. To conclude, the mental problems are divided into 3 categories, with schizophrenia and eating disorder having lower percentages, bipolar, alcohol and drug disorder having medium percentages, and depression, anxiety disorder having higher percentages. ")
    
    
    
    st.subheader("Percentage of Mental Problem Globally")
    col_77,col_78 = st.columns([2,5])
    melted_df1 = pd.melt(wp_mh,id_vars = ["entity","year"], value_vars = ['schizophrenia', 'bipolar', 'eating', 'anxiety','drug', 'depression', 'alcohol'], var_name = "mental_problem", value_name = "percent")
    
    fig15 = px.choropleth(melted_df1,locations="entity",locationmode="country names",color="percent",color_continuous_scale="sunset",projection="mollweide",facet_col='mental_problem', facet_col_wrap=2,title='Percentage of Mental Problems Globally',height=1200,width=1000)
    fig15.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    col_78.plotly_chart(fig15)
    col_77.markdown("This choropleth graph displays the distribution of mental problems in different continents. The colors shows the percentage value, with purple indicating higher values and yellow indicating lower values, we can understand which continents have a higher percentage of patients by observing the color of the region in the graph. However, in schizophrenia, bipolar disorder and eating disorder, the color of the continents are very similar, so we will focus on  analyzing the other mental problems. In the anxiety graph, the countries with the deepest color, purple, are the US, Brazil, Argentina, Australia, Iran and France. In the drug disorder graph, the countries with the deepest color, orange, are the US and Libya. In the depression graph, the country with the deepest color, warm purple, is Greenland. In the alcohol disorder graph, the country with the deepest color, light purple, is Russia. We can conclude that each mental problem have different favoring countries, and some of these countries we found are have the deepest colors for a reason. For example, Russia has the highest percentage of alcohol dependent population (Morris), leading to it being the country with the highest percentage of people with alcohol disorder. ")
    
    
    
    
    
    
    

if selected=="Focus analysis on different continents":
    st.title("Focus analysis on different continents")
    col_59,col_60 = st.columns([3,5])
    
    fig17 = px.box(wp_mh[wp_mh['entity'].isin(wp_mh[wp_mh["happiness_score"].notnull()]["entity"].unique())],x="region",y="happiness_score",color="region", labels=all_dict,color_discrete_sequence=rainbow,title="<b>Average of Happiness Score by Region<\b>",points="all")
    
    col_60.plotly_chart(fig17)
    col_59.markdown("Happiness Score by Region")
    col_59.markdown("This box plot is displaying the average of happiness scores of each year in each country, with the x-axis representing the regions and the y-axis representing the happiness score, we can obtain 2 different conclusions by observing this graph: the first one is range of the datapoints in each region, the second one is the mid point of each region which we can compare to find the region with the highest average happiness score. Let’s start by investigating the range of the datapoints. The region with the most diverse datapoints is Middle East and North Africa, with a maximum at 7.433 and a lowest at 2.688, which are almost the extremes of the dataset. The region with the most concentrated datapoints is West Asia, with a maximum of 6.853 and a minimum of 6.375. Other than the range of the datapoints, we can focus on the midpoints of the regions. The region with the lowest median happiness score is South-Saharan Africa, having a median score of 4.271. And the region with the highest median happiness score is North America and ANZ, having a median happiness score of 7.289. This shows that the regions have very diverse happiness scores, while every country in some regions have lower happiness scores, in other regions, every country has a higher happiness score. ")
    
    col_79,col_80 = st.columns([3,4])
    mental = ["schizophrenia","bipolar","eating","anxiety","drug","depression","alcohol"]
    def get_gosunburst(m):
        fig = px.sunburst(wp_mh,path =      ["region","entity"],values=m,color=m,color_continuous_scale="algae",height=5000,width=800)
        fig_dict = {k:fig.data[0][k] for k in   ["branchvalues","customdata","domain","hovertemplate","ids","labels","marker","name","parents","values"]}
        return fig_dict
    
    gosunbursts = {k:get_gosunburst(k) for k in mental}
    
    fig18 = make_subplots(
        rows=7, 
        cols=1, 
        specs=[
            [{"type":"domain"}],
            [{"type":"domain"}],
            [{"type":"domain"}],
            [{"type":"domain"}],
            [{"type":"domain"}],
            [{"type":"domain"}],
            [{"type":"domain"}]],
        subplot_titles=("Schizophrenia","Bipolar", "Eating Disorder","Anxiety","Drug    Disorder","Depression","Alcohol Disorder"),
        horizontal_spacing=0.05, 
        vertical_spacing=0.03)
    for i,(title,sun) in enumerate(gosunbursts.items()):
        r = i+1
        c = 1
        fig18.add_traces(go.Sunburst(**sun),rows=r,cols=c)
    fig18.update_layout(height=3000,width=1000)
    
    col_80.plotly_chart(fig18)
    col_79.subheader("Different Mental Problems by Region")
    col_79.markdown("This sunburst graph is displaying the distribution of percentage of mental problems in different regions. With each section displaying a different mental problem, all of the sections have all of the regions present and by clicking on the regions, we can examine the countries within this region and the percentage corresponding to the countries. The color scale shows the percentage of the mental problem, darker color means higher percentage and lighter color means lower percentage. However, the color continuous scale is not unified across the graphs. So, we can obtain two kinds of information from this graph: first, the sequence of the regions by percentage of the mental problem chosen, this can be obtained by observing the color of the inner circle of the sections; second, the sequence of the countries in the regions also sorted by color, this way we can see which country has the highest percentage of mental problem and which one has the lowest. Let’s observe the graphs one by one. ")
    col_79.markdown("Schizophrenia: The region with the darkest color is East Asia and Western Europe but we can see that East Asia has a higher average percentage by hovering on the region, 0.266% > 0.264%. The region with the lightest color is Sub-Saharan Africa, having a percentage of 0.168%. The country with the darkest color is Netherland (Western Europe)(0.372%) and Australia (North America and ANZ)(0.365%), the country with the lightest color is Mozambique (Sub-Saharan Africa) (0.151%). The region with the most diverse percentages is North America and ANZ, with a lowest at 0.174% (Trinidad and Tobago) and a highest at 0.365% (Australia). The region with the most concentrated percentages is Sub-Saharan Africa, with a lowest at 0.151% (Mozambique) and a highest at 0.234% (Mauritius).")
    col_79.markdown("Bipolar: The region with the darkest color is Western Europe with a percentage of 0.969%. The region with the lightest color is East Asia, having a percentage of 0.533%. The country with the darkest color is New Zealand (Northern America and ANZ)(1.199%), Northern Ireland (Western Europe)(1.143%), and Brazil (Latin America and Caribbean) (1.102%), the country with the lightest color is China (East Asia) (0.320%) and Papua New Guinea (North America and ANZ) (0.409%). The region with the most diverse percentages is North America and ANZ, with a lowest at 0.409% (Papua New Guinea) and a highest at 1.199% (New Zealand). The region with the most concentrated percentages is Sub-Saharan Africa, with a lowest at 0.561% (Mauritius) and a highest at 0.658% (Mauritania).")
    col_79.markdown("Eating Disorder: The region with the darkest color is Western Europe, having a percentage of 0.543%.The region with the lightest color is South Asia with a percentage of 0.127% and Sub-Saharan Africa with a percentage of 0.133%.  The country with the darkest color is Australia (Northern America and ANZ)(0.848%). The country with the lightest color is Somalia (South Africa) (0.078%) and Solomon Islands (North America and ANZ) (0.089%). The region with the most diverse percentages is North America and ANZ, with a lowest at 0.089% (Solomon Islands) and a highest at 0.848% (Australia).The region with the most concentrated percentages is South Asia, with a lowest at 0.095% (Afghanistan) and a highest at 0.144% (Bhutan).")
    col_79.markdown("Anxiety: The region with the darkest color is Western Europe, having a percentage of 5.695%. The region with the lightest color is Commonwealth of Independent States with a percentage of 2.694%.  The country with the darkest color is New Zealand (Northern America and ANZ)(8.657%) and Northern Ireland (Western Europe) (7.840%). The country with the lightest color is Tajikistan (Commonwealth of Independent States) (2.513%) and Mongolia (East Asia) (2.526%). The region with the most diverse percentages is North America and ANZ, with a lowest at 3.178% (Papua New Guinea) and a highest at 8.657% (New Zealand). The region with the most concentrated percentages is Commonwealth of Independent States, with a lowest at 2.513% (Tajikistan) and a highest at 2.942% (Russia).")
    col_79.markdown("Drug Disorder: The region with the darkest color is West Asia, having a percentage of 1.735%. The region with the lightest color is South Africa with a percentage of 0.572%. The country with the darkest color is the US (Northern America and ANZ)(2.881%). The country with the lightest color is Bosnia and Herzegovina (Central and Eastern Europe) (0.414%). The regions with the most diverse percentages are North America and ANZ, with a lowest at 0.679% (Vanuatu) and a highest at 2.881% (the US), and Middle East and North Africa, with a lowest at 0.461% (Guinea-Bissau) and a highest at 2.679% (United Arab Emirates). The region with the most concentrated percentages is South Africa, with a lowest at 0.466% (São Tomé and Principe) and a highest at 0.767% (Seychelles).")
    col_79.markdown("Depression: The region with the darkest color is Western Europe, having a percentage of 4.035%. The region with the lightest color is Southeast Asia with a percentage of 3.006%. The country with the darkest color is Greenland (Northern America and ANZ)(6.461%). The country with the lightest color is Albania (Central and Eastern Europe) (2.191%). The region with the most diverse percentages is North America and ANZ, with a lowest at 2.600% (Dominica) and a highest at 6.461% (Greenland). The region with the most concentrated percentages is West Asia, with a lowest at 3.441% (Oman) and a highest at 3.620% (Qatar).")
    col_79.markdown("Alcohol Disorder: The region with the darkest color is Commonwealth of   Independent States, having a percentage of 3.711%. The region with the lightest color is West Asia with a percentage of 0.696%. The country with the darkest color is Belarus (Commonwealth of Independent States)(5.292%). The country with the lightest color is Singapore (Southeast Asia) (0.480%). The region with the most diverse percentages is Commonwealth of Independent States, with a lowest at 1.966% (Georgia) and a highest at 5.292% (Belarus). The region with the most concentrated percentages is West Asia, with a lowest at 0.665% (Oman) and a highest at 0.725% (Qatar).")
    
    new_df = wp_mh[["region","year","sum"]].copy()

    col_81,col_82 = st.columns([4,5])
    for y in range(1990,2018):
        for r in ['South Asia', 'Central and Eastern Europe',
                  'Middle East and North Africa', 'North America and ANZ',
                  'Western Europe', 'South Africa', 'Latin America and Caribbean',
                  'Commonwealth of Independent States', 'Sub-Saharan Africa',
                  'Southeast Asia', 'East Asia', 'West Asia']:
            new_df.loc[(new_df["region"]==r) & (new_df["year"]==y),"sum"] =         new_df.loc[(new_df["region"]==r) & (new_df["year"]==y),"sum"].mean()
            #new_df.loc[(new_df["region"]=="South Asia") & (new_df["year"]==1990),"sum"]
            new_df.drop_duplicates()
    
    fig25 = px.line(new_df.sort_values("year"),x="year",y="sum",color="region", labels=all_dict,title="<b>Percentage of population who have mental problems by Year<\b>",markers=True)
    col_82.plotly_chart(fig25)
    col_81.subheader("Percentage of Mental Problems over the Years")
    col_81.markdown("This line graph displays the percentage of people who have mental problems by year, with the x-axis representing years from 1990-2015, and the y-axis representing the sum of the percentage of people who have mental problems. In this graph we can obtain two types of information, the first being the overall average percentage of the regions, the second one being the trend of the percentage over these 25 years. First, let’s dive into the graph and group the regions by the level of overall percentage. We can first observe that this graph has two outliers, Western Europe(purple) and Southeast Asia(grey), being the highest(13.8%) and the lowest(8.8%). We can then divide the remaining regions into 3 groups, with West Asia, North America and ANZ, Middle East & North Africa, Latin America and Caribbean as the second highest group, with an average percentage of 11.7%. The third highest group being Commonwealth of Independent States, Central Eastern Europe, and South Asia, with an average percentage of 10.5%. The second lowest group is composed of East Asia, South Africa and Sub-Saharan Africa, with an average percentage of 9.7%. After observing the groups the regions form on the graph, let’s now investigate the trends of the percentages over these 25 years. While some countries shows a stable trend, some shows a slight increase or decrease. Most of the regions have a stable trend, these include: Western Europe, North America and ANZ, Latin America and Caribbean, Commonwealth of independent states, South Asia, Sub-Saharan Africa, South Africa, and South East Asia. Some other regions shows a slight increase: Middle East and North Africa and East Asia. The rest of the regions shows a rather wiggling trend, the trend of West Asia shows an increase before 2000 and decreased soon after, finally reaching a stable trend; Central and Eastern Europe shows a decreasing trend before 2000 and starts to stabilize after that. ")
    

    
    
    


if selected=="Focus analysis on Canada, China, the US and UK":
    st.title("Focus analysis on Canada, China, the US and UK")
    
    col_57,col_58 = st.columns([1,1]) 
    melted_df2 = pd.melt(wp_mh[wp_mh['entity'].isin(["China","United States","United Kingdom","Canada"])],id_vars = ["entity","year"], value_vars =["happiness_score",
                      "economy",
                      "social_support",
                      "health",
                      "freedom",
                      "generosity"],
                         var_name = "happiness_index", value_name = "happiness_value")

    fig10=px.box(melted_df2,x="entity",y="happiness_value",color="entity",    labels=all_dict,title="Average of Happiness Indices",points="all",facet_col_spacing=0.05,facet_col = "happiness_index", facet_col_wrap =1,height=1000,width=1200)
    fig10.update_yaxes(matches=None,showticklabels=True)
    fig10.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    col_58.plotly_chart(fig10)
    col_57.subheader("Average of Happiness Indices")
    col_57.markdown("This box plot displays the average happiness indices over the years of Canada, China, the UK and the US. With the x-axis representing the different countries, and the y-axis representing the happiness indices percentage, we can notice not only the range of the datapoints but also the midpoints of the data that represents a country. Now, we can analyze the graphs in these two aspects. ")
    col_57.markdown("In the happiness score graph, China is the country with the most dispersive datapoints, while Canada being the country with the most condensed datapoints. The country with the highest mid-happiness score is Canada (7.422). The country with the lowest mid-happiness score is China (5.066), China has an especially low happiness score compared to other countries. ")
    col_57.markdown("In the economy graph, China is the country with the most dispersive datapoints, while the other countries all having condensed datapoints. The country with the highest mid-economy index is the US (10.931). The country with the lowest mid-economy index is China (9.214).")
    col_57.markdown("In the social support graph, the UK is the country with the most dispersive datapoints, while Canada being the country with the most condensed datapoints. The country with the highest mid-social support is the UK (0.952). The country with the lowest mid-social support is China (0.783).")
    col_57.markdown("In the health graph, China is the country with the most dispersive datapoints, while the US being the country with the most condensed datapoints. The country with the highest mid-health index is Canada (7.244). The country with the lowest mid-health index is China (6.784).")
    col_57.markdown("In the freedom graph, the UK is the country with the most dispersive datapoints, while Canada being the country with the most condensed datapoints. The country with the highest mid-freedom index is Canada(0.93). The country with the lowest mid-freedom index is China (0.81).")
    col_57.markdown("In the generosity graph, all countries have similar datapoint distributions. The country with the highest mid-generosity index is the UK(0.336). The country with the lowest mid-generosity index is China (-0.17).")
    col_57.markdown("To conclude our observations, we can see that China has the lowest datapoints in every happiness index. While the other countries are usually similar in range of data, but Canada is the one with the average highest datapoints. ")
    
    col_83,col_84 = st.columns([3,2])
    melted_df = pd.melt(wp_mh[(wp_mh['entity'].isin(["China","United States", "United Kingdom","Canada"]))&(wp_mh["year"]>2005)&(wp_mh["happiness_score"].notnull())],id_vars = ["entity","year"], value_vars = ['schizophrenia', 'bipolar', 'eating', 'anxiety','drug', 'depression', 'alcohol',"happiness_score"], var_name = "mental_problem", value_name = "percent")

    fig12 = px.line(melted_df,x="year",y="percent",color="entity", labels=all_dict,title="Average of Mental problem / Happiness Score by Year",facet_col='mental_problem', facet_col_wrap=1,height=1200,width=600,facet_col_spacing=0.05,facet_row_spacing = 0.1)
    fig12.update_yaxes(matches=None,showticklabels=True)
    fig12.update_xaxes(type="category")
    fig12.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
    col_84.plotly_chart(fig12)
    col_83.subheader("Average of Mental Problem / Happiness Score by Year")
    col_83.markdown("This graph presents the average percentages of various mental health issues and happiness scores across four countries (Canada, China, United Kingdom, and the United States) from 2007 to 2017. Here's a breakdown of the data:")
    col_83.markdown("Schizophrenia: The United States consistently has the highest percentage, around 0.34%. China and Canada show similar trends, maintaining around 0.32% and 0.30% respectively. The United Kingdom has the lowest rate, slightly below 0.30%.")
    col_83.markdown("Bipolar Disorder:The United States also leads in this category, with a percentage around 0.8%. Canada and China are close, with percentages around 0.6%. The United Kingdom has the lowest rate, around 0.4%.")
    col_83.markdown("Eating Disorders:The United States shows the highest rate, around 0.5%. Canada and China have similar rates, around 0.4% and 0.3% respectively. The United Kingdom has the lowest rate, just above 0.2%.")
    col_83.markdown("Anxiety: The United States has the highest percentage, around 7%. China and Canada are similar, with rates around 5% and 4% respectively. The United Kingdom has a slightly lower rate, around 3%.")
    col_83.markdown("Drug Use: The United States shows an increasing trend, peaking at around 7% in 2017. Canada and China have lower and more stable rates, around 4% and 2% respectively. The United Kingdom has the lowest rate, around 3%.")
    col_83.markdown("Depression: The United States has the highest rate, around 7%. Canada and China have similar rates, around 4% and 3.5% respectively. The United Kingdom has a slightly lower rate, around 4%.")
    col_83.markdown("Alcohol Use: The United States has the highest rate, around 2%. Canada and China have similar rates, around 1.5% and 1% respectively. The United Kingdom has the lowest rate, just below 1%.")
    col_83.markdown("Happiness Score: The United Kingdom generally has the highest happiness score, fluctuating around 7. Canada and China have similar scores, around 6.5 and 6 respectively. The United States has the lowest score, fluctuating around 5.5.")
    col_83.markdown("The United States consistently shows higher rates in mental health issues compared to the other countries. Canada and China have similar trends in most categories, with Canada generally having slightly higher rates. The United Kingdom tends to have lower rates in mental health issues but slightly lower happiness scores compared to Canada and China. Happiness scores in the UK are relatively stable and higher than in the other countries, despite having lower rates of some mental health issues.")
    
    
    col_85,col_86 = st.columns([3,5])
    melted_df3 = pd.melt(wp_mh[(wp_mh['entity'].isin(["China","United States", "United Kingdom","Canada"]))],id_vars = ["entity","year"], value_vars = ['schizophrenia', 'bipolar', 'eating', 'anxiety','drug', 'depression', 'alcohol'], var_name = "mental_problem", value_name = "percent")
    
    fig19 = px.histogram(melted_df3 ,x="entity",y="percent", labels=all_dict,histfunc="avg",barmode="group", title="<b>Average of Mental Problems in China, the US, the UK and Canada </b>",color="entity",facet_col = "mental_problem",facet_col_wrap=2,height=600,width=1200,facet_col_spacing=0.05)
    col_86.plotly_chart(fig19)
    col_85.subheader("Average of Mental Problems in China, Canada, the UK and the US")
    col_85.markdown("This graph presents the average percentages of various mental health issues across four countries: Canada, China, the United Kingdom, and the United States. Here's a breakdown of the data:")
    col_85.markdown("The United States generally has higher rates of mental health issues compared to the other countries, particularly in schizophrenia, bipolar disorder, eating disorders, anxiety, and drug use. Canada and the United Kingdom show similar trends in most categories, with Canada having slightly higher rates in anxiety and depression. China tends to have the lowest rates in most mental health issues, with the exception of anxiety, where it is on par with Canada and the UK. Alcohol use is relatively similar across all countries, with the United States having the highest rate at approximately 3%. This data suggests that while there are some commonalities in mental health issues across these countries, there are also significant differences that could be attributed to various factors such as cultural, social, and economic influences.")
    
    



if selected=="Conclusion":
    st.title("Conclusion")

    st.markdown("Based on the explorations and analysis, it is evident that mental health issues have a significant impact on the happiness indices of each country. The data reveals that countries with higher percentages of individuals experiencing mental health issues such as schizophrenia, bipolar disorder, eating disorders, anxiety, and depression tend to have lower happiness scores. Conversely, lower rates of these mental health issues are associated with higher happiness scores.")
    st.markdown("Among the mental health issues analyzed, anxiety and depression show a particularly strong negative correlation with happiness scores. This suggests that addressing these common mental health challenges could be a key strategy for improving national happiness levels. The United States, which has higher rates of several mental health issues, also tends to have lower happiness scores compared to countries like the United Kingdom, which has lower rates of these issues but higher happiness scores.")
    st.markdown("The analysis also highlights that while the United States generally has higher rates of mental health issues, it does not necessarily correlate with higher happiness scores. This indicates that the relationship between mental health and happiness is complex and may be influenced by other factors such as social support, economic conditions, and cultural attitudes towards mental health.")
    st.markdown("The distribution of mental health issues across different regions and countries further underscores the need for tailored approaches to mental health care. For instance, regions with higher rates of alcohol disorders or drug use may benefit from targeted interventions to address these specific issues.")
    st.markdown("In conclusion, the analysis provides valuable insights into the relationship between mental health and happiness across different countries. It suggests that improving mental health, particularly by addressing common issues like anxiety and depression, could significantly enhance happiness levels. However, it also highlights the importance of considering the unique mental health landscapes of different regions and countries when designing interventions. By understanding these relationships, policymakers and mental health professionals can develop more effective strategies to promote mental well-being and happiness on a global scale.")


if selected=="Bibliography":
    st.title("Bibliography")

    st.markdown("[1] Diener, Ed, and Tanya L. Chan. 'Happy People Live Longer: Subjective Well-Being Contributes to Health and Longevity.' Applied Psychology: Health and Well-Being, vol. 3, no. 1, 2011, pp. 1-43. ")
    st.markdown("[2] Keyes, Corey L. M. 'The Mental Health Continuum: From Languishing to Flourishing in Life.' Journal of Health and Social Behavior, vol. 43, no. 2, 2002, pp. 207-222. ")
    st.markdown("[3] Morris, Laura. “Alcoholism by Country Statistics [Our World in Data 2021].” Https://Www.abbeycarefoundation.com/, 2021, www.abbeycarefoundation.com/alcohol/alcoholism-by-country-statistics/.")
    st.markdown("[4] WHO. 'Mental Health: Strengthening Our Response.' World Health Organization, 2018, www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response. ")
    st.markdown("[5] Wood, Alex M., et al. 'The Role of Positive Mental Health in the Relationship Between Mental Health and Well-Being.' Journal of Happiness Studies, vol. 11, no. 2, 2010, pp. 251-273. ")




























