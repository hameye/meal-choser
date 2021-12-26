import ast
import requests
import streamlit as st
import pandas as pd
import numpy as np

# Get Sheet From Google API
r = requests.get(
    'https://sheets.googleapis.com/v4/spreadsheets/1aEK8c3xDDAetlMKmC11r37D82KRaq73bP7VGMgvETTU/values/sheet1?valueRenderOption=FORMATTED_VALUE&key=AIzaSyB1LRyMMyhUzs7ac8keUcBdBpEEHD-Zni8'
    ) 

# Convert bytes to dict and load as DataFrame
dictionnary = ast.literal_eval(r.content.decode('utf-8'))
df = pd.DataFrame(dictionnary['values'])
headers = df.iloc[0] 
new_df  = pd.DataFrame(df.values[1:], columns=headers) 

# Convert Columns Types
new_df['Distance'] = new_df['Distance'].astype(float)


st.title('Meal Choser')

# Filter Genre
genre = st.radio(
    "Do you want a hot or cold meal",
    ('Hot', 'Cold'))
new_df = new_df[new_df['Hot/Cold'] == genre]



# Filter Here or Togo
where_options = np.unique(new_df['Here/ToGo'])
if len(where_options) > 1: 
    where = st.radio(
        "Do you want here or to go",
        ('Here', 'ToGo'), index=1)
    new_df = new_df[new_df['Here/ToGo'] == where]



# Filter Distance
dist_min = float(new_df['Distance'].min())
dist_max = float(new_df['Distance'].max())
if dist_max != dist_min:
    values = st.slider(
        'Select the distance range',
        dist_min, dist_max, (dist_min, dist_max))
    new_df = new_df[new_df['Distance'] >= values[0]]
    new_df = new_df[new_df['Distance'] <= values[1]]

    

# Filter type of food
food_options = np.unique(new_df['Type'])
if len(food_options) > 1:
    options = st.multiselect(
        'What kind of food do you want',
        food_options)

if st.button('Compute Location'):
    if len(new_df) > 1:
        st.write(
            f" The Meal Choser chosed for you : {new_df.sample(1)['Nom'].iloc[0]} :yum:")
    elif len(new_df) == 1:
        st.write(f" You chosed : {new_df['Nom'].iloc[0]} :yum:")
    else:
        st.write("You are too difficult to satisfy :weary:")
