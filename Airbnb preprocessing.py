#********************************************************************************Importing Libraries****************************************************************************************************************************************
import pandas as pd
import pymongo
import matplotlib.pyplot as plt
import seaborn as sb
#************************************************************************************************************************************************************************************************************************
#connecting mongo_DB
ragul = pymongo.MongoClient("mongodb+srv://ragul_s:raguldesire@cluster0.l7eucom.mongodb.net/?retryWrites=true&w=majority")
#****************************************************************************Connecting airbnb********************************************************************************************************************************************
db = ragul["sample_airbnb"]
col = db["listingsAndReviews"]
#***********************************************************************************Viewing all rows and columns*************************************************************************************************************************************
pd.set_option('display.max_columns', None)
#**********************************************************************************preprocessing**************************************************************************************************************************************
Data = []

for i in col.find( {}, {'id':1, 'listing_url':1, 'name':1, 'description':1, 'house_rules':1, 'property_type':1, 'room_type':1,
                        'bed_type':1, 'minimum_nights':1, 'maximum_nights':1, 'cancellation_policy':1, 'accommodates':1,
                        'bedrooms':1, 'beds':1, 'price':1, 'security_deposit':1, 'cleaning_fee':1,
                        'extra_people':1, 'guests_included':1, 'number_of_reviews':1,'review_scores.review_scores_rating':1,
                        'bathrooms':1, 'amenities':1} ):
    Data.append(i)

df = pd.DataFrame(Data)
df['review_scores'] = df['review_scores'].apply(lambda x: x.get('review_scores_rating',0))
df.isnull().sum()
#***************************************************************************************Fill missing values*********************************************************************************************************************************
#Filling the missing value
df['bedrooms'].fillna(0,inplace=True)
df['beds'].fillna(0,inplace=True)
df['bathrooms'].fillna(0,inplace=True)
df['cleaning_fee'].fillna(0,inplace=True)
df['security_deposit'].fillna(0,inplace=True)
#************************************************************************************************************************************************************************************************************************
# Filling Empty values in Description and House rules columns
df.description.replace(to_replace='',value='No Description Provided',inplace=True)
df.house_rules.replace(to_replace='',value='No House rules Provided',inplace=True)
df.amenities.replace(to_replace='',value='Not Available',inplace=True)
df.isnull().sum()
#checking data types
df.dtypes
#***************************************************************************************Checking datatypes*********************************************************************************************************************************
df['minimum_nights'] = df['minimum_nights'].astype(int)
df['maximum_nights'] = df['maximum_nights'].astype(int)
df['beds'] = df['beds'].astype(int)
df['bathrooms'] = df['bathrooms'].astype(str).astype(float)
df['price'] = df['price'].astype(str).astype(float).astype(int)
df['extra_people'] = df['extra_people'].astype(str).astype(float).astype(int)
df['guests_included'] = df['guests_included'].astype(str).astype(int)
df['cleaning_fee'] = df['cleaning_fee'].astype(str).astype(float).astype(int)
df['security_deposit'] = df['security_deposit'].astype(str).astype(float)

df.dtypes
#*************************************************************************************Connecting host***********************************************************************************************************************************
# host
host = []

for i in col.find( {}, {'id':1, 'host':1}):
    host.append(i)

df_host = pd.DataFrame(host)
host_keys = list(df_host.iloc[0,1].keys())
host_keys.remove('host_about')

for i in host_keys:
    if i == 'host_response_time':
        df_host['host_response_time'] = df_host['host'].apply(lambda x: x['host_response_time'] if 'host_response_time' in x else 'Not Specified')
    else:
        df_host[i] = df_host['host'].apply(lambda x: x[i] if i in x and x[i]!='' else 'Not Specified')

df_host.drop(columns=['host'], inplace=True)
df_host.head()

df_host['host_is_superhost'] = df_host['host_is_superhost'].map({False:'No',True:'Yes'})
df_host['host_has_profile_pic'] = df_host['host_has_profile_pic'].map({False:'No',True:'Yes'})
df_host['host_identity_verified'] = df_host['host_identity_verified'].map({False:'No',True:'Yes'})
df_host.isnull().sum()
#***********************************************************************************Connecting address*************************************************************************************************************************************
#address

add = []
for i in col.find( {}, {'id':1, 'address':1}):
    add.append(i)

df_add = pd.DataFrame(add)
address_keys = list(df_add.iloc[0,1].keys())

for i in address_keys:
    if i == 'location':
        df_add['location__type'] = df_add['address'].apply(lambda x: x['location']['type'])
        df_add['longitude'] = df_add['address'].apply(lambda x: x['location']['coordinates'][0])
        df_add['latitude'] = df_add['address'].apply(lambda x: x['location']['coordinates'][1])
        df_add['is_location_exact'] = df_add['address'].apply(lambda x: x['location']['is_location_exact'])
    else:
        df_add[i] = df_add['address'].apply(lambda x: x[i] if x[i]!='' else 'Not specified')
df_add.drop(columns=['address'], inplace=True)
df_add['is_location_exact'] = df_add['is_location_exact'].map({False:'No',True:'Yes'})
df_add.head(3)
df_add.isnull().sum(),df_add.dtypes
#******************************************************************************************Connecting availability******************************************************************************************************************************
#Availablity
availability = []
for i in col.find( {}, {'_id':1, 'availability':1}):
    availability.append(i)

df_availability = pd.DataFrame(availability)
df_availability

availability_keys = list(df_availability.iloc[0,1].keys())

for i in availability_keys:
    df_availability['availability_30'] = df_availability['availability'].apply(lambda x: x['availability_30'])
    df_availability['availability_60'] = df_availability['availability'].apply(lambda x: x['availability_60'])
    df_availability['availability_90'] = df_availability['availability'].apply(lambda x: x['availability_90'])
    df_availability['availability_365'] = df_availability['availability'].apply(lambda x: x['availability_365'])

df_availability.drop(columns=['availability'], inplace=True)
df_availability.head()
df_availability.isnull().sum(),df_availability.dtypes
df = pd.merge(df, df_host, on='_id')
df = pd.merge(df, df_add, on='_id')
df = pd.merge(df, df_availability, on='_id')
df.dtypes
#*************************************************************************************Convert it into Dataframe***********************************************************************************************************************************
#Converting dataframe to csv file and saving it
df.to_csv('Airbnb_data.csv',index=False)
            

